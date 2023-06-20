import socket
import os 

buffer_size = 1024

# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e a porta que o servidor estará conectado
HOST, PORT = 'localhost', 8000 #eolicagepoc.ct.ufsm.br / localhost
print(f'Iniciando conexão com o servidor em {HOST}:{PORT}')

# Conecta o socket ao endereço IP e porta do servidor
client_socket.connect((HOST, PORT))

# Recebe os nomes dos arquivos disponíveis para download 
files = list() 

file = client_socket.recv( 1024 ) 

# Mostra os arquivos disponíveis para download
print( 'Os arquivos disponíveis para download são:' )
print( file.decode() )

# Envia a mensagem para o servidor solicitar um arquivo
file_name = input('\nDigite o nome do arquivo que deseja fazer download: ')
client_socket.send(f'GET {file_name}'.encode())

# Caminho para fazer download dos arquivos 
download_path = os.path.dirname( __file__ ) + '/downloads/' 

counter = 0
acum_data_transfer = 0

# Abre o arquivo para escrita
with open( download_path + file_name, 'wb') as f:
    # Recebe os pacotes de dados do servidor
    while True:
        data = client_socket.recv(buffer_size)
        if data == b'OK':
            break
        else:
            counter += 1 
            data_size = len(data)
            acum_data_transfer += data_size
            print( f'Recebido o segmento número {counter} com {data_size} bytes - Número de bytes do arquivo recebidos: {acum_data_transfer}')
        f.write(data)

# Fecha o socket
client_socket.close()
