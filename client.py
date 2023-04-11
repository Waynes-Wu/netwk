import socket
import os
import json
# * ---------- GLOBAL VAR----------------
USERINPUT = ''
INPSPLIT = []
HANDLE = None

# serverAddressPort = ('localhost', 2000)
serverAddressPort = None
CLIENTSOCKET = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
bufferSize = 1024
# * ---------------FUNCTIONS-------------
def clear():
    os.system('cls')

def sendJSON(dictionary):
    json_str = json.dumps(dictionary)
    CLIENTSOCKET.sendto(json_str.encode(), serverAddressPort)

    response = CLIENTSOCKET.recv(1024).decode()
    return response

def askCommand():
    a = input('>>> ')
    return a

def welcome():
    print('--------------------------')
    print('|  Message Board System  |')
    print('--------------------------')
    print()
    print('type \'/?\' for list of commands')

def join():
    """/join <server_ip_add> <port>"""
    success_message = 'Connection to the Message Board Server is successful!'
    tempDict = {"command":"join"}

    global serverAddressPort 
    serverAddressPort= (INPSPLIT[1], int(INPSPLIT[2]))
    try:
        CLIENTSOCKET.connect(serverAddressPort)
        print(success_message)
    except Exception as e:
        print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
    
    response = sendJSON(tempDict)
    return


def leave():
    success_message = 'Connection closed. Thank you!'
    tempDict = {"command":"leave"}

    response = sendJSON(tempDict)
    CLIENTSOCKET.close()
    print(success_message)
    return

def register():
    global USERHANDLE
    USERHANDLE = INPSPLIT[1]
    success_message = f'Welcome {USERHANDLE}!'
    tempDict = {"command":"register", "handle": INPSPLIT[1]}
    return

def send_all():
    # success_message = f'{handle}: {message}'
    tempDict = {"command":"all", "message": INPSPLIT[1]}
    pass

def send_handle():
    # success_message = f'[To {receiver}] : {message}'
    tempDict = {"command":"msg", "handle":INPSPLIT[1], "message":INPSPLIT[2]}    
    pass

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


welcome()


# # ! DEBUG
# serverAddressPort = ('localhost', 2000)
# CLIENTSOCKET.connect(serverAddressPort)
# tempDict = {"command":"join"}
# sendJSON(tempDict)



while True:
    # main runs here

    USERINPUT = askCommand()
    INPSPLIT = USERINPUT.split()

    # clear()

    # --------------'SWITCH CASE'--------------------------
    tempDict = {}
    if INPSPLIT[0] == '/join':
        join()

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