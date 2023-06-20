import socket

serverAddressPort   = ("127.0.0.1", 9876)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Define um timeout 
UDPClientSocket.settimeout( 10 )  

msg = input('Enter message to send : ')

# Send to server using created UDP socket
UDPClientSocket.sendto(str.encode(msg), serverAddressPort)


print('\nWaiting server return message\n')
msgFromServer = UDPClientSocket.recvfrom(bufferSize)


msg = "Message received from Server: {} ".format(msgFromServer[0].decode())


print(msg)
print("Ending application... bye")