'''
Author: Bruno Gabriel Flores Sampaio 
Date: 01/04/2023 
Title: Monitoria de Redes Industriais UFSM 2023.1 
Description: Código para transmissão [i]Streamer[/i] de imagem da câmera 
servidor/cliente utilizando o loopback via TCP 
'''

import _thread 
import socket
import cv2 

HOST = 'localhost'
PORT = 12345

MAX_CONNECTIONS = 5
INDEX_CAM = 0 

clients = []


def listen_clients(): 
    global clients 

    # Inicia o soquete no tipo SOCK_STREAM = TCP
    server = socket.socket( socket.AF_INET,socket.SOCK_STREAM ) 

    # Vincula o soquete 
    server.bind( (HOST, PORT) )

    # Define o número máximo de conexões 
    server.listen( MAX_CONNECTIONS ) 

    while True: 
        print( 'Waiting for clients: ')
        connection, addr = server.accept( ) 

        print( f'Connected at: {addr[0]} with port {addr[1]}' )

        # Adiciona o cliente à lista de clientes 
        clients.append( [ connection, addr ] )



def send_to_clients( frame ):
    global clients 
    # Codifica a imagem em bytes 
    _, frame_encode = cv2.imencode( '.jpg', frame )

    # Percorre todos os clientes conectados 
    for n, (conn, addr) in enumerate(clients):
        try: 
            # Envia todos os bytes da mensagem para o cliente
            conn.sendall( frame_encode )
        except:
            # Se o cliente se desconectou, então exclui ele da lista 
            clients.pop(n)


# Inicia a busca por clientes conectados
_thread.start_new_thread( listen_clients, () )

# Video capture object 
vid = cv2.VideoCapture( INDEX_CAM )

while(True):
    # Lê a camera 
    ret, frame = vid.read()

    # # Mostra o frame 
    # cv2.imshow('frame', frame)

    # # Preciona 'Q' para sair 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Envia o frame para os clientes 
    send_to_clients( frame )


# After the loop release the cap object
vid.release()

# Destroy all the windows
cv2.destroyAllWindows()




'''
Outras fontes são https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b 
'''