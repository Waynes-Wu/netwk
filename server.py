import socket
import json

# ! -------------------------------------------------------------
def sendJSON(dictionary):
    json_str = json.dumps(dictionary)
    SERVERSOCKET.sendto(json_str.encode(), serverAddressPort)
# ! -------------------------------------------------------------

serverAddressPort = ("127.0.0.1", 2000)
bufferSize = 1024

SERVERSOCKET = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
SERVERSOCKET.bind(serverAddressPort)

print("UDP server up and listening")
print(f'opening a server in {serverAddressPort}')

# ! -------------------------------------------------------------
clients = {}
while (True):

    statusReturn = {'message' : ''}

    receivingMsg, address = SERVERSOCKET.recvfrom(bufferSize)
    print(f'client {address} has sent a message')
    
    # we will be referring to client ass port, since this is localhost
    port = address[1]

    cmdDict = json.loads(receivingMsg.decode())

    command = cmdDict.get('command')
    # ! -- join  --------------------
    if command == 'join':
        a = clients.get(port)
        if a == None:
            clients[port] = ''
        print('new client joined')
        statusReturn['message'] = 'Connection to the Message Board Server is successful!'

    # ! -- leave -------------------
    if command == 'leave':
        del (clients[port])
        print('removed a client')
        statusReturn['message'] = 'Connection closed. Thank you!'

    # ! -- register ----------------
    if command == 'register':
        newHandle = cmdDict.get('handle')

        # conditions here is if it's not taken
        if clients.get(port) == '':
            clients[port] = newHandle
            statusReturn['message'] = f'Welcome {newHandle}!'

    # ! -- send all  --------------
    if command == 'all':
        message = cmdDict.get('message')
        sender = clients.get(port)

        message = f'{sender} : {message}'

        for key in clients.keys():
            if key == port:
                continue
            SERVERSOCKET.sendto(message.encode(), ("127.0.0.1", key))
            statusReturn['message'] = f'[To all] : {message}'


    # ! -- send to handle
    if command == 'msg':
        message = cmdDict.get('message')
        handle = cmdDict.get('handle')
        sender = clients.get(port)
        sent = False
        for key, value in clients.items():
            if (value == handle) and (key != port):

                message = f'[From {sender} : {message}]'

                try:
                    SERVERSOCKET.sendto(message.encode(), ("127.0.0.1", "127.0.0.1", key))
                    sent = True
                except:
                    pass

        # good message
        if sent:
            statusReturn['message'] = f'[To {value}] : {message}'




    statusReturn = json.dumps(statusReturn)
    SERVERSOCKET.sendto(statusReturn.encode(), address)

    
    # if (len(clients) == 0):
    #     break
SERVERSOCKET.close()

