import _thread 
import socket

import os
PATH =  os.path.dirname( __file__ )
DONWLOAD_PATH = PATH + '/downloads'


HOST = 'localhost'
PORT = 12345

MAX_CONNECTIONS = 5


def multi_threaded_client( connection : socket, count : int = 0 ) -> None:
    file_to_download = open( f"{DONWLOAD_PATH}/img_down_{count}.png", "wb")
    while True:
        data = connection.recv(1024)
        if data == b"DONE":
                print("Done Receiving.")
                break
        file_to_download.write( data )
    file_to_download.close()
    
    connection.send( "Thank you for connecting".encode() )
    connection.shutdown(2)
    connection.close()


def main():
    sock = socket.socket() 
    sock.bind( (HOST, PORT) )
    sock.listen( MAX_CONNECTIONS ) 
    count = 0 

    while True: 
        print( 'Esperando a conexão' )
        connection, addr = sock.accept()

        _thread.start_new_thread( multi_threaded_client, ( connection, count, ) )
        
        print( 'Connected {} with IP {} '.format( addr[0], addr[1] ) )
        print( 'Thread Number: ' + str( count ) )
        count += 1 


if __name__ == '__main__':
     main() 