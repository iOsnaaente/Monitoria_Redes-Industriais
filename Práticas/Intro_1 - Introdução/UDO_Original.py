import socket 

# Cria um socket TCP/IP
client_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
client_socket.settimeout( 1 )

# Define o endereço e a porta do servidor
IP, PORTA = '192.168.0.255', 9876

# Lê a mensagem do usuário
message = input('> ')

# Envia a mensagem para o servidor
client_socket.send( message.encode('utf-8') )

# Função que fica aguardando o recebimento de novas mensagens 
while True: 
    try:
        data = socket.recv(1024)
        print( data.decode(), end = '\n>' ) 
    except socket.error as e:
        print( e )
