import socket
import os 

# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e a porta que o servidor estará conectado
HOST, PORT = 'localhost', 8000
print(f'Iniciando conexão com o servidor em {HOST}:{PORT}')

# Conecta o socket ao endereço IP e porta do servidor
client_socket.connect((HOST, PORT))

# Recebe os nomes dos arquivos disponíveis para download 
files = list() 
while True: 
    file = client_socket.recv( 1024 ) 
    if b'EOF' in file :
        break
    else:
        files.append( file )

# Mostra os arquivos disponíveis para download
print( 'Os arquivos disponíveis para download são:' )
for file in files:
    print( file.decode() )

# Envia a mensagem para o servidor solicitar um arquivo
file_name = input('\nDigite o nome do arquivo que deseja fazer download: ')
client_socket.send(f'GET {file_name}'.encode())

# Caminho para fazer download dos arquivos 
download_path = os.path.dirname( __file__ ) + '/downloads/' 

# Abre o arquivo para escrita
with open( download_path + file_name, 'wb') as f:
    # Recebe os pacotes de dados do servidor
    while True:
        data = client_socket.recv(15000)
        if data == b'OK':
            break
        f.write(data)

# Fecha o socket
client_socket.close()
