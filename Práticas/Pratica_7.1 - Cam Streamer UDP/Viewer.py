import numpy as np 
import socket
import cv2 

HOST = 'localhost'
PORT = 12345

MAX_BYTE_LEN = 15000

# Inicia o arquivo socket 
client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

# Define um tempo de timeout para a conexão
client.settimeout( 1 )

# Solicita conexão 
client.connect( (HOST, PORT) )
client.send( b'Request cam access' )

while True:
    try: 
        # Recebe os bytes do servidor
        frame = b''
        while True:
            recv = client.recv( MAX_BYTE_LEN )
            if recv == b'done':
                break
            else:
                frame += recv 
                
        # Converte os bytes em um array de bytes ordenados
        frame = np.asarray( bytearray( frame ), dtype = "uint8" )
        # Decodifica os bytes de forma que o CV2 possa entender 
        frame = cv2.imdecode( frame, cv2.IMREAD_COLOR)

        # Desenha parametros de FPS e aquisição dos pacotes 

        # Mostra o frame no display CV2 
        cv2.imshow('Image received from server', frame)

        # Se pressionado a tecla Q encerra o processo 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except:
        continue