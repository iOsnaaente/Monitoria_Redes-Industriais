import socket

MAX_CONNECTION = 1

IP   = '127.0.0.1'
PORT = 12345

server = socket.socket(  socket.AF_INET, socket.SOCK_STREAM )

server.bind( (IP, PORT) ) 
server.listen( MAX_CONNECTION )

print( f'Iniciando o socket no endereço {IP}:{PORT}')
print(  'Pronto para iniciar conexões com novos clientes')

while True: 
    print(  'Aguardando conexão....' )
    connection, addr = server.accept()
    
    print( f'Cliente {addr[0]}:{addr[1]}' )
    while True:
        # Aguarda o recebimento de novas conexões 
        data = connection.recv( 1024 )  
        print( f'Recebido do lado cliente: {data}')

        # Encerra o código caso não receba nada 
        if not data:
            break 
        # Caso receba, retorna um echo da mensagem 
        else: 
            print( 'Retornando ECHO')
            connection.send( data )
