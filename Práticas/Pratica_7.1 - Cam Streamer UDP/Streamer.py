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

MAX_BYTE_LEN = 15000
MAX_CONNECTIONS = 5
INDEX_CAM = 0 

clients = []

# Inicia o soquete no tipo SOCK_DGRAM = UDP 
server = socket.socket( socket.AF_INET, socket.SOCK_DGRAM  ) 
# Vincula o soquete 
server.bind( ( HOST, PORT ) )


def listen_clients( sock : socket.socket ): 
    global clients 

    while True: 
        print( 'Waiting for clients identify: ')
        msg, addr = sock.recvfrom( 1024 ) 
        # Validando solicitação de acesso 
        if msg == b'Request cam access':
            print( f'Connected at: {addr[0]} with port {addr[1]}: {msg}' )
            # Adiciona o cliente à lista de clientes 
            clients.append( addr )


def send_to_clients( frame, sock : socket.socket ):
    global clients 
    # Codifica a imagem em bytes 
    _, frame_encode = cv2.imencode( '.jpg', frame )
    # Percorre todos os clientes conectados
    for n, addr in enumerate(clients):
        try: 
            # Envia todos os bytes da mensagem para o cliente
            length = len( frame_encode )
            for n in range(length//MAX_BYTE_LEN):     
                sock.sendto( frame_encode[ MAX_BYTE_LEN*n : MAX_BYTE_LEN*(n+1)], addr )
            sock.sendto( frame_encode[MAX_BYTE_LEN*((length//MAX_BYTE_LEN)) : ], addr )
            sock.sendto( b'done', addr )
        except:
            # Se o cliente se desconectou, então exclui ele da lista 
            clients.pop(n)


# Inicia a busca por clientes conectados
_thread.start_new_thread( listen_clients, (server, ) )

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
    send_to_clients( frame, server )


# After the loop release the cap object
vid.release()

# Destroy all the windows
cv2.destroyAllWindows()




'''
Outras fontes são https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b 
'''