#Alvin Onabolu
#Nahor Yirgaalem

# Import socket module

from socket import * 
import struct
import sys
import time

CLIENT = 1
SERVER = 2

def check_server_response(response):
    data_len, pcode, entity = struct.unpack_from('!IHH', response)
    if pcode==555:
        response = response[8:]
        print(response.decode())
        sys.exit()
    return 

def phaseA(clientSocket, server_name, server_port):
    #packet should contain pcode, entity, data length, data
    pcode = 0
    entity = CLIENT 
    data = 'Hello World!!!00'
    #returns size of string in bytes
    data_length = len(data.encode())


    #pack data, into packet
    header = struct.pack('!IHH', data_length, pcode, entity)
    packet = header + data.encode('utf-8')
  

    #Send the packet(bytes) to server address
    clientSocket.sendto(packet, (server_name, server_port))


    #receiving response back from server
    try:
        response, serverAddress = clientSocket.recvfrom(2048)
    except:
        print("Client did not receive any packet back for phase A...")
        clientSocket.close()
        sys.exit()
    data_length, pcode, entity, repeat, udp_port, length, codeA = struct.unpack('!IHHIIHH', response)

    print(f'Received packet from server: data_len: {data_length}  pcode: {pcode}  entity: {entity}  repeat: {repeat}  len: {length}  udp_port: {udp_port}  codeA: {codeA}')
  
    return repeat, udp_port, length, codeA


def phaseB(clientSocket, server_name, server_port, repeat, length, pcode):
    #Assign variables
    entity = CLIENT
 
    
    #make lenght divisible by 4
    while length % 4 != 0:
        length += 1

    data = bytearray(length) 

    # 4 is the length of packet id
    data_length = len(data) + 4

    
    #send repeat number of packets
    for packet_id in range(repeat):
        packet = struct.pack(f'!IHHI{length}s', data_length, pcode, entity, packet_id, data)
        print(f'Sending packet with packet ID: {packet_id}')
     
        clientSocket.sendto(packet, (server_name, server_port))
        
        #try to receive ack packet if no receive keep on resending packet
        failed = True
        while (failed):
            try:
                response, serverAddress = clientSocket.recvfrom(2048)
            except:
                #This except block will hit if timeout eeror on socket
                print("Did not receive ack packet from server...")
                print(f'Resending packet with packet id: {packet_id}')
                packet = struct.pack(f'!IHHI{length}s', data_length, pcode, entity, packet_id, data)
                clientSocket.sendto(packet, (server_name, server_port))
            else:
                failed = False


        s_data_length, pcode, s_entity, s_packet_id = struct.unpack('!IHHI', response)
        print(f'Received acknowledgement packet from server: data_len:  {s_data_length} pcode:  {pcode} entity:  {s_entity} acknumber:  {s_packet_id}')

    #Once received all ack packets from server wait to receive final packet
    try:
        response, serverAddress = clientSocket.recvfrom(2048)
    except:
        print("Did not receive final packet from server")
        clientSocket.close()
        sys.exit()
    


    data_length, pcode, entity, tcp_port, codeB = struct.unpack('!IHHII', response)
    print(f'Received final packet: data_len:  {data_length} pcode:  {pcode} entity: {entity} tcp_port: {tcp_port}  codeB: {codeB}')

    return tcp_port, codeB
        
        






def phaseD(clientSocket):
    #receive packet from server
    packet = clientSocket.recv(1024)
 
    data_length, pcode, entity, repeat2, length2, codeC, char = struct.unpack('!IHHIIIB', packet)

    print(f'Received packet from server: data_len: {data_length}  pcode: {pcode}   entity: {entity}   repeat2: {repeat2}   len2: {length2}   codeC: {codeC}   char:  {char}')
    print('------------ End of Stage C  ------------\n')
    
    
    #send repeat2 number of packets to server
    #make lenght divisible by 4
    while length2 % 4 != 0:
        length2 += 1

    pcode = codeC


    #create our data for our packets
    arr = length2 * [char]

    
    data = bytearray(arr)

    print(f'sending  {data[:8]} to server for {repeat2} times')
  

    #send repeat2 number of packets
    for packet_id in range(repeat2):
        packet = struct.pack(f'!IHH{length2}s', length2, pcode, CLIENT, data)
        print(f'Sending packet with packet ID: {packet_id}')
        clientSocket.send(packet)
    


    try:
        response = clientSocket.recv(2048)
    except:
        print("Did not receive final packet from server")
        clientSocket.close()
        sys.exit()

    
    #check_server_response(response)
    data_length, pcode, entity, codeD = struct.unpack('!IHHI', response)


    print(f'Received from server: data_len: {data_length}  pcode: {pcode}  entity: {entity}  codeD: {codeD}')
    
    
    return


#Create Socket
server_name = '34.69.60.253' #use ip address of computer u want to connect to
#server_name = 'localhost' #use ip address of computer u want to connect to

server_port = 12000
# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_DGRAM)
#incase server runs into error and doesnt send nothing 
clientSocket.settimeout(5)

print('------------ Starting Stage A  ------------')
repeat, udp_port, length, codeA = phaseA(clientSocket, server_name, server_port)
print('------------ End of Stage A  ------------\n')


print('------------ Starting Stage B  ------------')

server_port = udp_port
tcp_port, codeB = phaseB(clientSocket, server_name, server_port, repeat, length, codeA)
print('------------ End of Stage B  ------------\n')



print('------------ Starting Stage C  ------------')
#Connect to tcp port PhaseC
print(f'connecting to server at tcp port {tcp_port}')
clientSocket.close()
server_port = tcp_port
clientSocket = socket(AF_INET, SOCK_STREAM)
time.sleep(3)
clientSocket.settimeout(5)
clientSocket.connect((server_name, server_port))



phaseD(clientSocket)
print('------------ End of Stage D  ------------\n')


print("Done All phases Closing...")
clientSocket.close()
sys.exit()



