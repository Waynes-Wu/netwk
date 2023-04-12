import socket
import os
import json
# * ---------- GLOBAL VAR----------------
USERINPUT = ''
INPSPLIT = []
HANDLE = None
THREAD = True
serverAddressPort = None
CLIENTSOCKET = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
bufferSize = 1024
# * ---------------FUNCTIONS-------------

# def clear():
#     os.system('cls')

def sendJSON(dictionary):
    json_str = json.dumps(dictionary)
    CLIENTSOCKET.sendto(json_str.encode(), serverAddressPort)
    global THREAD
    THREAD = False

    response = CLIENTSOCKET.recv(1024).decode()

    data = json.loads(response)

    THREAD = True

    return data.get('status')

def askCommand():
    a = input('>>> ')
    return a

def welcome():
    print('--------------------------')
    print('|  Message Board System  |')
    print('--------------------------')
    print()
    print('type \'/?\' for list of commands')

# ! -- join
def join():
    """/join <server_ip_add> <port>"""
    success_message = 'Connection to the Message Board Server is successful!'
    tempDict = {"command":"join"}

    global serverAddressPort 

    try:
        serverAddressPort= (INPSPLIT[1], int(INPSPLIT[2]))
    except:
        print('Error: Command parameters do not match or is not allowed.')
        return


    try:
        CLIENTSOCKET.connect(serverAddressPort)
    except Exception as e:
        serverAddressPort = None
        print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
    
    response = sendJSON(tempDict)

    if response:
        print(success_message)

    return

# ! -- leave
def leave():

    if len(INPSPLIT > 1):
        print('Error: Command parameters do not match or is not allowed.')
        return

    # ? CONNECTED
    if serverAddressPort == None:
        print('Error: Disconnection failed. Please connect to the server first.')
        return

    success_message = 'Connection closed. Thank you!'
    tempDict = {"command":"leave"}

    response = sendJSON(tempDict)
    if response:
        serverAddressPort = None
        print(success_message)
    return

# ! -- register
def register():

    global HANDLE
    try:
        HANDLE = INPSPLIT[1]
    except:
        print('Error: Command parameters do not match or is not allowed.')
        return
    
    # ? CONNECTED
    if serverAddressPort == None:
        print('Error: Disconnection failed. Please connect to the server first.')
        return

    tempDict = {"command":"register", "handle": HANDLE}
    success_message = f'Welcome {HANDLE}!'


    response = sendJSON(tempDict)
    if response:
        print(success_message)
    else: 
        print('Error: Registration failed. Handle or alias already exists.')

    return

# ! -- send all
def send_all():

    message = INPSPLIT[1]

    # ? CONNECTED
    if serverAddressPort == None:
        print('Error: Please connect to the server first.')
        return
    
    # ? not registered
    if HANDLE == '':
        print('Error: Please register before sending a message.')
        return

    success_message = f'{HANDLE}: {message}'
    tempDict = {"command":"all", "message": INPSPLIT[1]}
    response = sendJSON(tempDict)   

    if response:
        print(success_message)
    else:
        print('Error: Handle or alias not found.')



# ! -- send to handle
def send_handle():

    # ? CONNECTED
    if serverAddressPort == None:
        print('Error: Disconnection failed. Please connect to the server first.')
        return
    
    # ? not registered
    if HANDLE == '':
        print('Error: Please register before sending a message.')
        return
    
    message = INPSPLIT[2]
    success_message = f'[To {INPSPLIT[1]}] : {message}'
    tempDict = {"command":"msg", "handle":INPSPLIT[1], "message":message} 
    response = sendJSON(tempDict)   
    if response:
        print(success_message)


# !-- help
def help():
    print(
'''
    List of commands
    ~ to connect to the server app
        /join <server_ip_add> <port>
    ~ to disconnect from the server app
        /leave
    ~ register a unique handle
        /register <handle> 
    ~ send message to all
        /all <message>
    ~ send a direct message
        /msg <handle> <message>
    ~ get list of commands
        /?
''')

import threading
def receive_messages():
    while True:
        if THREAD:
            data = CLIENTSOCKET.recvfrom(1024)
            data = json.loads(data[0].decode())

            if data.get('command') == 'message':
                # {message: message, sender: handle}
                message = data.get('message')
                sender = data.get('sender')
                print(f'[From {sender}] : {message}')


receive_thread = threading.Thread(target=receive_messages)


welcome()




while True:
    # main runs here

    USERINPUT = askCommand()
    INPSPLIT = USERINPUT.split()

    print('---------')

    # --------------'SWITCH CASE'--------------------------
    tempDict = {}
    if INPSPLIT[0] == '/join':
        join()
        receive_thread.start()
        

# * NEEDS TO BE CONNECTED

    elif INPSPLIT[0] == '/leave':
        leave()

    elif INPSPLIT[0] == '/register':
        register()

    elif INPSPLIT[0] == '/all':
        send_all()
        
    elif INPSPLIT[0] == '/msg':
        send_handle()


    elif INPSPLIT[0] == '/?':
        help()
    # -----------AFTER 'SWITCH CASE'----------------------
    



# expect and print out status of command

# msgFromClient       = "Hello UDP Server"

# bytesToSend         = str.encode(msgFromClient)

# serverAddressPort   = ("127.0.0.1", 20001)

# bufferSize          = 1024

# # Create a UDP socket at client side
# UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# # Send to server using created UDP socket
# UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# msgFromServer = UDPClientSocket.recvfrom(bufferSize)

# msg = "Message from Server {}".format(msgFromServer[0])

# print(msg)

