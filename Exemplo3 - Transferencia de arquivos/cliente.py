import socket
import os 

# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e a porta que o servidor estará conectado
HOST, PORT = 'localhost', 8000
print(f'Iniciando conexão com o servidor em {HOST}:{PORT}')

# Conecta o socket ao endereço IP e porta do servidor
client_socket.connect((HOST, PORT))

# Envia a mensagem para o servidor solicitar um arquivo
file_name = input('Digite o nome do arquivo para fazer download: ')
client_socket.send(f'GET {file_name}'.encode())

# Caminho para fazer download dos arquivos 
download_path = os.path.dirname( __file__ ) + '/downloads/' 

# Abre o arquivo para escrita
with open( download_path + file_name, 'wb') as f:
    # Recebe os pacotes de dados do servidor
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        f.write(data)

# Fecha o socket
client_socket.close()
