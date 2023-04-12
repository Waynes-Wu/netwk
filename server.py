import socket
import json


serverAddressPort = ("127.0.0.1", 2000)
bufferSize = 1024


msgFromServer = "Hello UDP Client"


# Create a datagram socket

SERVERSOCKET = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
SERVERSOCKET.bind(serverAddressPort)


def sendJSON(dictionary):
    json_str = json.dumps(dictionary)
    SERVERSOCKET.sendto(json_str.encode(), serverAddressPort)


print("UDP server up and listening")
print(f'opening a server in {serverAddressPort}')


# Listen for incoming datagrams
clients = {}
while (True):

    # LIST OF COMMANDS
    # 	join, leave 					--(no need send command?)
    #   register, send all, send priv	--(expect to receive these)
    # message_received = SERVERSOCKET.recvfrom(bufferSize)
    # message_received

    # what i think will happen join means add the address to list
    # leave means remove from list
    # maybe save a list of dictionary for the addresses or at least another dictionary for name and addresses

    success = False

    receivingMsg = SERVERSOCKET.recvfrom(bufferSize)
    print(f'connected -- {receivingMsg[1]}')
    port = receivingMsg[1][1]

    commandingMsg = json.loads(receivingMsg[0].decode())

    command = commandingMsg.get('command')
    # ! -- join
    if command == 'join':
        try:
            clients[port] = ''
            success = True
        except:
            success == False
        print('new client joined')
        print('  ', clients)

    # ! -- leave
    if command == 'leave':
        del (clients[port])


    # ! -- register
    if command == 'register':
        newHandle = commandingMsg.get('handle')

        try:
            clients[port] = newHandle
            success = False
        except:
            success = False

    # ! -- send all
    if command == 'all':
        message = commandingMsg.get('message')
        for key in clients.keys():
            SERVERSOCKET.sendto(message.encode(), ("127.0.0.1", key))

    # ! -- send to handle
    if command == 'msg':
        message = commandingMsg.get('message')
        handle = commandingMsg.get('handle')

        try:
            for key, value in clients.items():
                if (value == handle) and (key != port):
                    SERVERSOCKET.sendto(message.encode(), ("127.0.0.1", "127.0.0.1", key))
            success = True
        except:
            success = False

    # send back to sender
    status_dict = {}
    status_dict['status'] = success
    status_dict = json.dumps(status_dict)
    SERVERSOCKET.sendto(status_dict.encode(), receivingMsg[1])

    if (len(clients) == 0):
        break
SERVERSOCKET.close()
