from cryptography.fernet import Fernet
import threading
import socket 


# Cria um socket TCP/IP
client_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

# Define o endereço e a porta do servidor
IP, PORTA = 'localhost', 8000

# Conecta ao servidor
client_socket.connect( (IP, PORTA) )

# Armazena a chave de criptografia única  
#   gerada pelo servidor 
UNIQUE_KEY = client_socket.recv( 1024 )

# Gera o encriptador Fernet 
f = Fernet( UNIQUE_KEY )

# Responde um b'OK' criptografado para sinalizar 
#   o recebimento da chave 
client_socket.send( f.encrypt( b'OK' ) )

# Função que fica aguardando o recebimento de novas mensagens 
def listen( socket : socket ): 
    while True: 
        # Recebe os dados do servidor 
        data = socket.recv(1024)
        # Quebra a criptografia dos dados 
        data = f.decrypt( data )
        # Transforma o bytearray em str 
        data = data.decode() 
        # Printa na tela a mensagem
        print( data , end = '\n>' ) 

# Se sincronizou, inicia uma Thread para ficar ouvindo o servidor 
client_listen = threading.Thread( target = listen, args = (client_socket, ) )
client_listen.start() 

while True:
    # Lê a mensagem do usuário
    message = input('> ')
    # Envia a mensagem para o servidor
    client_socket.send( f.encrypt( message.encode() ) )