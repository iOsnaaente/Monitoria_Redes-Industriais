import threading 
import socket
import os 

buffer_size = 1024

# Cria um socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço e a porta que o socket vai se vincular
IP, PORT = '0.0.0.0', 8000
print(f'Iniciando servidor em {IP}:{PORT}')
server_socket.bind((IP, PORT))

# Define o número máximo de clientes que podem se conectar
server_socket.listen(5)

# Caminho absoluto para o diretório das imagens
files_path = os.path.dirname( __file__ ) + '/files/'

print(files_path)

# Pega os arquivos disponíveis na pasta files 
files = os.listdir(files_path)
# Adiciona um marcador de fim de lista End Of File 
print( 'Arquivos disponíveis: ')
arquivos = ""
for file in files:
    arquivos += file + "\n"
print(arquivos)

# Função para tratar a comunicação com cada cliente paralelamente 
def receive_file( client_socket ):

    # Envia os nomes dos arquivos disponíveis 
    client_socket.send( arquivos.encode() )

    # Recebe a mensagem do cliente
    data = client_socket.recv(1024)
    
    # Verifica se o cliente solicitou um arquivo
    if data.startswith(b'GET'):
    
        # Obtém o nome do arquivo solicitado
        file_name = data.split()[1].decode()
        print( f'Cliente solicitou o arquivo {file_name}' )
        
        # Verifica se o arquivo existe
        if file_name in files:
            print(f'Arquivo {file_name} encontrado.')
            file_stats = os.stat(files_path + file_name)
            #print(file_stats)
            print(f'File Size in Bytes is {file_stats.st_size}')
            print(f'File Size is %.1f kB' % (file_stats.st_size / (1024)))
            #print(f'File Size in MegaBytes is {file_stats.st_size / (1024 * 1024)}')

            data_size = 0
            acum_data_transfer = 0

            # Abre o arquivo para leitura
            with open( files_path + file_name, 'rb') as f:
                # Envia o arquivo em pacotes de 1024 em 1024 bytes
                count = 0
                while True:
                    data = f.read(buffer_size)
                    if not data:
                        break
                    else: 
                        count += 1 
                        data_size = len(data)
                        acum_data_transfer += data_size
                        print( f'Enviado o segmento número {count} com {data_size} bytes')
                        print( f'Transferido {acum_data_transfer} de {file_stats.st_size} bytes - %.1f %%' % (100 * acum_data_transfer / file_stats.st_size))
                        client_socket.send(data)

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
