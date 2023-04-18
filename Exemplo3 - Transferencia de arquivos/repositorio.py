import threading 
import socket
import os 

# Cria um socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e a porta que o socket vai se vincular
IP, PORT = 'localhost', 8000
print(f'Iniciando servidor em {IP}:{PORT}')
server_socket.bind((IP, PORT))

# Define o número máximo de clientes que podem se conectar
server_socket.listen(5)

# Caminho absoluto para o diretório das imagens
img_path = os.path.dirname( __file__ ) + '/imagens/'

# Função para tratar a comunicação com cada cliente paralelamente 
def receive_file( client_socket ):

    # Recebe a mensagem do cliente
    data = client_socket.recv(1024)
    
    # Verifica se o cliente solicitou um arquivo
    if data.startswith(b'GET'):
    
        # Obtém o nome do arquivo solicitado
        file_name = data.split()[1].decode()
        print( f'Cliente solicitou o arquivo {file_name}' )
        
  # Verifica se o arquivo existe
        if file_name in [
            'cachorro.jpg', 	
            'gato.jpg', 	
            'iguana.jpg', 
            'tucano.jpg' 
        ]:
            
            print(f'Arquivo {file_name} encontrado.')
            # Abre o arquivo para leitura
            with open( img_path + file_name, 'rb') as f:
                # Envia o arquivo em pacotes de 1024 em 1024 bytes
                count = 0
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    client_socket.send(data)
                    count += 1 
                    print( f'Enviado o segmento número {count}')

            # Envia uma mensagem final para o cliente 
            print('Envio concluído' )
            client_socket.send( b'OK' )

        # Se o arquivo não existe, encerra a conexão 
        else:
            # Caso o arquivo não exista
            print( f'Arquivo {file_name} NÃO encontrado.' )
            data = f'ERROR "O arquivo {file_name} não existe"'            
            client_socket.send( data.encode() )
    # Fecha a conexão com o cliente
    client_socket.close()
  
while True:
    # Aceita a conexão do cliente
    print('Aguardando conexão...')
    client_socket, client_address = server_socket.accept()
    
    print(f'Cliente conectado: {client_address[0]}:{client_address[1]}')
    
    # Recebe o arquivo enviado pelo cliente
    client = threading.Thread(   
        target = receive_file, 
        args = ( client_socket, ) 
    )
    client.start() 
