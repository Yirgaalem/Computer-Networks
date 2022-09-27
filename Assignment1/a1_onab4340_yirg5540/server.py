#Alvin Onabolu
#Nahor Yirgaalem

# Import socket module

import code
from socket import * 
import struct
import sys
import time
import random


CLIENT = 1
SERVER = 2




def closeConnection(serverSocket):
    serverSocket.close()
    print("Server Closed.")
    sys.exit()




def phaseA(serverSocket):


    #Receiving packet from client
    try:
        packet, clientAddress = serverSocket.recvfrom(1024)
    except:
        print("Timeout has occured, closing server...")
        closeConnection(serverSocket)
        

    #Checking socket termination conditions
    try:  
        #If we werent sent correct number of argument in packet, a struct error would be raised
        data_length, pcode, entity, word = struct.unpack('!IHH16s', packet)
        word = word.decode('utf-8')

        #Check that all value are correct, and packet is divisble by 4
        if (data_length != 16 or pcode != 0 or entity != 1 or word != "Hello World!!!00" or len(packet) != 24):
            #close Conection 
            print("incorrect value")
            closeConnection(serverSocket)
    except struct.error:
        #close connection
        print("Incorrect number of arguments")
        closeConnection(serverSocket)

    

    #collect Hello World message
    word = word[:-2]

    print(f'receiving from the client: data_length: {data_length} code: {pcode}  entity: {entity} data: {word}\n')

    print('------------ Starting Stage A  ------------\n')
    #create new packet to send back to client
    repeat = 2#random.randint(5,20)
    udp_port = random.randint(20000, 30000)
    length = random.randint(50, 100)
    codeA = random.randint(100, 400)
    entity = SERVER


    #Repeat is 4 bytes, udp port is 4 byts, + length is 2, codeA is 2
    data_length = 12

    print(f'sending to the client: data_length: {data_length}  code: {pcode} entity: {entity}  repeat: {repeat}  udp_port: {udp_port}  len: {length} codeA: {codeA}')


    #Put header details back to bytes ensure this has big endian
    packet = struct.pack('!IHHIIHH', data_length, pcode, entity, repeat, udp_port, length, codeA)
  

    #send packet back to client
    serverSocket.sendto(packet, clientAddress)

    #return the udpport to be listened to for next phase
    return udp_port, repeat, length, codeA



def verify_phaseD_packet(i, char, connectionSocket, serverSocket, length2, codeC):
    #Receiving packet from client
    try:
        packet = connectionSocket.recv(1024)
    except:
        print("Timeout has occured for phase B, closing server...")
        connectionSocket.close()
        closeConnection(serverSocket)
        

    #Checking socket termination conditions
    try:  
        #If we werent sent correct number of argument in packet, a struct error would be raised
        data_length, pcode, entity, data = struct.unpack(f'!IHH{length2}s', packet)
 

        #Check that all value are correct, and packet is divisble by 4
        if (data_length != (length2) or pcode != codeC or entity != CLIENT or data_length % 4 != 0):
            #close Conection 
            print("incorrect value")
            connectionSocket.close()
            closeConnection(serverSocket)

    except struct.error:
        #close connection
        print("Incorrect number of arguments")
        connectionSocket.close()
        closeConnection(serverSocket)


    print(f' i =  {i} data_len:  {data_length} pcode:  {pcode} entity:  {entity} data:  {data[:8]}')

    

def verify_phaseB_packet(serverSocket, order, length, codeA):
    #Receiving packet from client
    try:
        packet, clientAddress = serverSocket.recvfrom(1024)
    except:
        print("Timeout has occured for phase B, closing server...")
        closeConnection(serverSocket)
        

    #Checking socket termination conditions
    try:  
        #If we werent sent correct number of argument in packet, a struct error would be raised
        data_length, pcode, entity, packet_id, data = struct.unpack(f'!IHHI{length}s', packet)

        #Check that all value are correct, and packet is divisble by 4
        if (len(data) != length or data_length != (length + 4) or pcode != codeA or entity != CLIENT or packet_id != order or data_length % 4 != 0):
            #close Conection 
            print("incorrect value")
            closeConnection(serverSocket)
    except struct.error:
        #close connection
        print("Incorrect number of arguments")
        closeConnection(serverSocket)

    print(f'SERVER: received_packet_id =  {packet_id} data_len =  {data_length}  pcode: {pcode}')

    return clientAddress


def send_ack(serverSocket, pcode, order, clientAddress):

    #4 reps that order/data length will be 4 bytes
    packet = struct.pack('!IHHI', 4, pcode, SERVER, order)
    serverSocket.sendto(packet, clientAddress)



def phaseB(serverSocket, repeat, pcode, length):
    #used to check if packets maintain order
    order = 0

    #get the correct length of what the len variable should be with padding
    while length % 4 != 0:
        length += 1


    #Continously listen and send ack packets to client
    while True:
        #receive packet from client, might have to change time out so that it is higher than clients timeout
        clientAddress = verify_phaseB_packet(serverSocket, order, length, pcode)
        #choose whether to send back ack packet or not
        send = random.randint(0,1)
        if (send == 1):
            print(f'SERVER: Sending Ack packet to client for packet id: {order}')
            send_ack(serverSocket, pcode, order, clientAddress)
            order +=1 
        #stop sending packets once we have received repeat number of packets
        if (order == repeat):
            break
    
    #send final packet for phase B
    tcp_port = random.randint(20000, 30000)
    codeB = random.randint(100, 400)
    data_length = 8 #tcp port is 4 bytes and code b are both 4byte integer
    packet = struct.pack('!IHHII', data_length, pcode, SERVER, tcp_port, codeB)
    serverSocket.sendto(packet, clientAddress)

    print(f' ------------- B2: sending tcp_port {tcp_port} codeB {codeB}')

    return tcp_port, codeB






def phaseC(connectionSocket, serverSocket, pcode):
    #create packet to send to client
    repeat2 = 2#random.randint(5,20)
    length2 = random.randint(50, 100)
    codeC = random.randint(100, 400)
    char = 'A'
    char = char.encode('utf-8')
    data_length = 4 + 4 + 4 + 1
    packet = struct.pack('!IHHIIIc', data_length, pcode, SERVER, repeat2, length2, codeC, char)
    print(f'Server Sending to the client:  data_length: {data_length} code: {pcode}  entity: 2  repeat2: {repeat2}  len2: {length2} codeC:  {codeC}')
    connectionSocket.send(packet)
    return repeat2, length2, codeC, char


def phaseD(connectionSocket, serverSocket, repeat2, length2, codeC, char):

    
    #get the correct length of what the len variable should be with padding
    while length2 % 4 != 0:
        length2 += 1


    print('Starting to Receive packets from client')
    #Continously receive client packets to client
    for i in range(repeat2):
        #receive packet from client, might have to change time out so that it is higher than clients timeout
        verify_phaseD_packet(i, char, connectionSocket, serverSocket, length2, codeC)

    codeD = random.randint(100, 400)
    data_length = 4 #code d is 4 bytes
    packet = struct.pack('!IHHI', data_length, codeC, SERVER, codeD)
    connectionSocket.send(packet)
    return
   
 
    



# Assign a port number
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to server address and server port
#no ip address cause we want to receive messages from any computer
serverSocket.bind(("", serverPort))

#Ensure that time out is 3 second if port was listening
serverSocket.settimeout(3.0)

#Executing phases one at a time while keeping connection open
while True:
    serverPort, repeat, length, codeA = phaseA(serverSocket)
    #Create new socket with new udp port
    serverSocket.close()
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(("", serverPort))
    serverSocket.settimeout(7.0)

    print(f'SERVER: Server ready on the new UDP port: {serverPort}')
    print('SERVER:------------ End of Stage A  ------------\n\n')


    print('SERVER:------------ Starting Stage B  ------------')
    tcp_port, codeB = phaseB(serverSocket, repeat, codeA, length)
    print(' ------------ End of Stage B  ------------\n')


    print(' ------------ Stating Stage C ------------')
    # Creat tcp connection
    serverSocket.close()
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverPort = tcp_port
    serverSocket.bind(("", serverPort))
    serverSocket.settimeout(7.0)
    print(f'The server is ready to receive on tcp port: {serverPort}')
    # Listen for connection
    serverSocket.listen(5)
    connectionSocket, addr = serverSocket.accept()
    
    
    repeat2, length2, codeC, char = phaseC(connectionSocket, serverSocket, codeB)
    print(' ------------ End of Stage C    ------------\n')

    print(' ------------ Starting Stage D  ------------')
    phaseD(connectionSocket, serverSocket, repeat2, length2, codeC, char)
    print('Finished Phase D.')
    print('Closing Program')
    connectionSocket.close()
    #close the socket and server once all phases are done 
    closeConnection(serverSocket)

