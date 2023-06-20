'''
Author: Bruno Gabriel Flores Sampaio 
Date: 01/04/2023 
Title: Monitoria de Redes Industriais UFSM 2023.1 
Description: Código para recepção [i]Streamer[/i] de imagem da câmera 
servidor/cliente utilizando o loopback via TCP 
'''
import numpy as np 
import socket
import cv2 

HOST = 'localhost'
PORT = 12345

# Inicia o arquivo socket 
client = socket.socket()

# Define um tempo de timeout para a conexão
client.settimeout( 1 )

# Solicita conexão 
client.connect( (HOST, PORT) )

count = 0
while True:
    try: 
        # Recebe os bytes do servidor 
        frame = client.recv( 240000 )
        # Converte os bytes em um array de bytes ordenados
        frame = np.asarray( bytearray( frame ), dtype = "uint8" )
        # Decodifica os bytes de forma que o CV2 possa entender 
        frame = cv2.imdecode( frame, cv2.IMREAD_COLOR)

        # Desenha parametros de FPS e aquisição dos pacotes 

        # Mostra o frame no display CV2 
        cv2.imshow('Image received from server', frame)
        print( f'frame {count}')
        count += 1 

        # Se pressionado a tecla Q encerra o processo 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except:
        continue