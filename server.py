import socket
import json


serverAddressPort = ("127.0.0.1", 2000)
bufferSize  = 1024



msgFromServer       = "Hello UDP Client"




# Create a datagram socket

SERVERSOCKET = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
SERVERSOCKET.bind(serverAddressPort)

def sendJSON(dictionary):
    json_str = json.dumps(dictionary)
    SERVERSOCKET.sendto(json_str.encode(), serverAddressPort)


print("UDP server up and listening")



# Listen for incoming datagrams

while(True):

# LIST OF COMMANDS
# 	join, leave 					--(no need send command?)
#   register, send all, send priv	--(expect to receive these)
	# message_received = SERVERSOCKET.recvfrom(bufferSize)
	# message_received


# what i think will happen join means add the address to list 
# leave means remove from list
# maybe save a list of dictionary for the addresses or at least another dictionary for name and addresses




    bytesAddressPair = SERVERSOCKET.recvfrom(bufferSize)

    message = bytesAddressPair[0].decode

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)



    # # Sending a reply to client

    SERVERSOCKET.sendto(msgFromServer.encode(), address)
    break