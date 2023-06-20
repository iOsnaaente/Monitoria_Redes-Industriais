import _thread
import socket

MAX_CONNECTION = 1

IP = '127.0.0.1'

APP1 = 50505 
APP2 = 50506
APP3 = 50507


def listen_socket( sock : socket.socket, sock_name : str ): 
    print( f'Init socket echo named: {sock_name}')
    while True: 
        connection, addr = sock.accept()
        print( f'[{sock_name}]Connected {addr[0]} with IP {addr[1]}' )
        while True:
            data = connection.recv( 10240 )        
            if not data:
                break 
            else: 
                print( data )
                connection.send( data )

if __name__ == '__main__':
    echo_app1 = socket.socket(  socket.AF_INET, socket.SOCK_STREAM )
    echo_app1.bind( (IP, APP1) ) 
    echo_app1.listen( MAX_CONNECTION )
    _thread.start_new_thread( listen_socket, ( echo_app1, 'ECHO APP1', ) )
    
    echo_app2 = socket.socket(  socket.AF_INET, socket.SOCK_STREAM )
    echo_app2.bind( (IP, APP2) ) 
    echo_app2.listen( MAX_CONNECTION )
    _thread.start_new_thread( listen_socket, ( echo_app2, 'ECHO APP2', ) )
    
    echo_app3 = socket.socket(  socket.AF_INET, socket.SOCK_STREAM )
    echo_app3.bind( (IP, APP3) ) 
    echo_app3.listen( MAX_CONNECTION )
    listen_socket( echo_app3, 'ECHO APP3' )