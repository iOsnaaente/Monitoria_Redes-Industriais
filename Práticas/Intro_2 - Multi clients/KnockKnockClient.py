# Socket client example in python

import socket   # for sockets
import sys  	# for exit

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

print('Socket Created')

host = 'localhost'
port = 4444

try:
    remote_ip = socket.gethostbyname( host )

except socket.gaierror:
    # could not resolve
    print('Hostname could not be resolved. Exiting' ) 
    sys.exit()

# Connect to remote server
s.connect((remote_ip , port))

print('Socket Connected to ' + host + ' on ip ' + remote_ip)

while True:
	server_msg = s.recv(1024)

	print("Sever: " + server_msg.decode())

	if server_msg.decode() == "Bye.":
		break

	# Send some data to remote server
	client_msg = input('Enter message to send : ')

	try :
		# Set the whole string
		s.sendall( bytes( client_msg, 'ascii' ) ) 
			
	except socket.error:
		# Send failed
		print('Send failed')
		sys.exit()