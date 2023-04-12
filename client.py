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

# have no gotten = false
PROMISE = False
RESPONSE = ''
# * ---------------FUNCTIONS-------------

# def clear():
#     os.system('cls')

def sendJSON(dictionary):
    json_str = json.dumps(dictionary)
    CLIENTSOCKET.sendto(json_str.encode(), serverAddressPort)
    return

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

    if len(INPSPLIT) != 3:
        print('Error: Command parameters do not match or is not allowed.')
        return
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
    
    sendJSON(tempDict)
    global PROMISE
    global RESPONSE
    global THREAD
    while not PROMISE:
        continue
    PROMISE = False

    if RESPONSE:
        print(success_message)

    return

# ! -- leave
def leave():
    global serverAddressPort 
    if len(INPSPLIT) != 1:
        print('Error: Command parameters do not match or is not allowed.')
        return
    
    # ? CONNECTED
    if serverAddressPort == None:
        print('Error: Disconnection failed. Please connect to the server first.')
        return

    success_message = 'Connection closed. Thank you!'
    tempDict = {"command":"leave"}

    sendJSON(tempDict)

    global PROMISE
    global RESPONSE
    
    while not PROMISE:
        continue
    PROMISE = False

    if RESPONSE:
        serverAddressPort = None
        print(success_message)
    return

# ! -- register
def register():
    global serverAddressPort 
    global HANDLE

    if len(INPSPLIT) != 2:
        print('Error: Command parameters do not match or is not allowed.')
        return
    
    # ? CONNECTED
    if serverAddressPort == None:
        print('Error: Disconnection failed. Please connect to the server first.')
        return

    HANDLE = INPSPLIT[1]
    tempDict = {"command":"register", "handle": HANDLE}
    success_message = f'Welcome {HANDLE}!'


    sendJSON(tempDict)

    global PROMISE
    global RESPONSE
    
    while not PROMISE:
        continue
    PROMISE = False

    if RESPONSE:
        print(success_message)
    else: 
        print('Error: Registration failed. Handle or alias already exists.')

    return

# ! -- send all
def send_all():
    global serverAddressPort 

    if len(INPSPLIT) != 2:
        print('Error: Command parameters do not match or is not allowed.')
        return
    
    # ? CONNECTED
    if serverAddressPort == None:
        print('Error: Please connect to the server first.')
        return
    
    # ? not registered
    if HANDLE == '':
        print('Error: Please register before sending a message.')
        return

    message = INPSPLIT[1]
    success_message = f'{HANDLE}: {message}'
    tempDict = {"command":"all", "message": INPSPLIT[1]}
    sendJSON(tempDict)   

    global PROMISE
    global RESPONSE
    
    while not PROMISE:
        continue
    PROMISE = False

    if RESPONSE:
        print(success_message)
    else:
        print('Error: Handle or alias not found.')



# ! -- send to handle
def send_handle():

    if len(INPSPLIT) != 3:
        print('Error: Command parameters do not match or is not allowed.')
        return
    
    global serverAddressPort 
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
    sendJSON(tempDict)  

    global PROMISE
    global RESPONSE
    
    while not PROMISE:
        continue
    PROMISE = False

    if RESPONSE:
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
        data = CLIENTSOCKET.recvfrom(1024)
        data = json.loads(data[0].decode())

        if data.get('command') == 'message':
            # {message: message, sender: handle}
            message = data.get('message')
            sender = data.get('sender')
            print(f'[From {sender}] : {message}')
        global PROMISE
        PROMISE = True


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
    else:
        if INPSPLIT[0][0] == '/':
            print('Error: No command was found.')
        else:
            print('Error: Invalid command.')
 

