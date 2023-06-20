import threading 
import socket
import sys

from KnockKnockProtocol import KnockKnockProtocol

HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
PORT = 4444         # Arbitrary non-privileged port
msg  = ""

protocol = KnockKnockProtocol()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
    s.bind( (HOST, PORT) )
except socket.error:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

s.listen(10)
print('Server is now listening')


# Função para lidar com as conexões de clientes
def handle_client( conn, addr ):
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    # Cria o primeiro pacote para enviar ao cliente 
    server_msg = protocol.processInput("")
    conn.sendall( bytes( server_msg, 'ascii' ) )

    # Mantem uma conversa com o cliente
    while True:
        data = conn.recv( 1024 )
        print( "Client: " + data.decode() )

        server_msg = protocol.processInput( data.decode() )
        conn.sendall( bytes( server_msg,'ascii' ) )
        print( server_msg )

        if server_msg == "Bye.":
            break


# Inicia o servidor para escutar os novos clientes 
while True:

    # Aguarda novas conexões 
    conn, addr = s.accept()
    thr = threading.Thread( target = handle_client, args = (conn, addr, ) )
    thr.start() 
    

conn.close()
s.close()
