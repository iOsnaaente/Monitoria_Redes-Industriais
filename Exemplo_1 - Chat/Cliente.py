import threading
import socket

# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e a porta do servidor
IP, PORTA = 'localhost', 8000

# Conecta ao servidor
client_socket.connect( (IP, PORTA) )

# Função que fica aguardando o recebimento de novas mensagens 
def listen( socket : socket ): 
    while True: 
        data = socket.recv(1024)
        print( data.decode(), end = '\n>' ) 

# Inicia uma Thread para ficar ouvindo o servidor 
client_listen = threading.Thread( target = listen, args = (client_socket, ) )
client_listen.start() 

while True:
    # Lê a mensagem do usuário
    message = input('> ')

    # Envia a mensagem para o servidor
    client_socket.send( message.encode('utf-8') )

    print()
