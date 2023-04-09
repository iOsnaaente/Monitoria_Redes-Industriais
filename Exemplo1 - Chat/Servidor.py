import socket
import threading

# Cria um socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )

# Define o endereço e a porta que o socket vai se vincular
# O endereço dos sockets em python é realizado via tupla (IP, PORT)
IP, PORT = 'localhost', 8000

print( f'Iniciando servidor em {IP}:{PORT}' )
server_socket.bind( (IP, PORT) )

# Escuta as conexões definindo o número de clientes que podem se conectar
server_socket.listen(5)

# Lista para armazenar os clientes conectados
clients = []

# Função para enviar uma mensagem para todos os clientes conectados
def broadcast( message ):
    for client in clients:
        client.send(message)

# Função para lidar com as conexões de clientes
def handle_client( client_socket, client_address ):
    # Adiciona o cliente à lista de clientes conectados
    clients.append(client_socket)
    while True:
        try:
            # Recebe a mensagem do cliente
            message = client_socket.recv(1024)
            if message:
                # Envia a mensagem para todos os clientes conectados
                broadcast(message)
            else:
                # Remove o cliente da lista de clientes conectados
                clients.remove( client_socket )
                client_socket.close()
                break
        except:
            # Remove o cliente da lista de clientes conectados caso ocorra algum erro
            clients.remove(client_socket)
            client_socket.close()
            break

while True:
    print( 'Aguardando conexão...')
    
    # Aceita a conexão do cliente
    client_socket, client_address = server_socket.accept()

    # Inicia uma thread para lidar com a conexão do cliente
    # Roda casa solicitação paralelamente 
    client_thread = threading.Thread( target = handle_client, args = ( client_socket, client_address ) )
    client_thread.start()
