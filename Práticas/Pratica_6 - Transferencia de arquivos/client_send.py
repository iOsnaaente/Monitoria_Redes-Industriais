# Pegar o diretório do arquivo
import os 
PATH = os.path.dirname( __file__ )

# Importar a biblioteca dos soquetes 
import socket
HOST = 'localhost'
PORT = 12345


def send_file( file_path : str, sock : socket ) -> bool:
    file_to_send = open( file_path, "rb" )
    try: 
        data = file_to_send.read(1024)
        count = 1
        while data:
            print( "Sending... Segm: ", count )
            count += 1 
            sock.send( data ) 
            data = file_to_send.read( 1024 )
        file_to_send.close()
        sock.send(b"DONE")
        return True 
    except:
        return False 


def main():
    # Iniciar o soquete  
    sock = socket.socket()
    # Esperar os soquetes por 0.1s
    sock.settimeout( 0.1 ) 
    sock.connect( ( HOST, PORT ) )
    # Inicia o envio de um arquivo 
    send_file( f'{PATH}/universo.png', sock )
    print("Done Sending")
    # Recebe a resposta 
    print( sock.recv(1024).decode() )
    sock.close()


if __name__ == "__main__":
    main() 