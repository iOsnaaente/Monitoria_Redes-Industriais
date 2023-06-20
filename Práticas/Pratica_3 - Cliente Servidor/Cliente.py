import socket

IP   = '127.0.0.1'
PORT = 12345  
 
client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
while True: 
    data = input('Digite uma mensagem para enviar ao servidor: ' )
    
    print( f'Enviando ao servidor {IP}:{PORT}: {data}')
    client.sendall( data.encode() )
    
    recv = client.recv(1024)
    print( f'Recebido: {recv}')
