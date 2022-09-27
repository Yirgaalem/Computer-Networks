# Import socket module
from socket import * 
import sys # In order to terminate the program

serverName = '10.84.97.64'

# Assign a port number
serverPort = 12000

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_DGRAM)
sentence = 'This is a message from tobi ' #this is our data

#clientSocket.connect((serverName, serverPort))
clientSocket.sendto( sentence.encode(), (serverName, serverPort))

#receiving back from server
modifiedSentence, serverAddress = clientSocket.recvfrom(2048)

#print server address backd
print('From server: ', modifiedSentence.decode())
clientSocket.close()
