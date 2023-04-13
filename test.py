import socket
import threading
import json

sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort = None
receive_thread = None

# ! ----------------WRAPPERS----------------------------
def connection_req(func):
    def wrapper(*args, **kwargs):
        global sock
        if sock.getsockname() == ('0.0.0.0', 0):
            print('Error: Please connect to the server first.')
            return
        return func(*args, **kwargs)
    return wrapper

def register_req(func):
    def wrapper(*args, **kwargs):
        # Check the condition here
        if sock.getsockname() == ('0.0.0.0', 0):
            print('Error: Please connect to the server first.')
        else:
            return func(*args, **kwargs)
    return wrapper

def check_args(n):
    def length_decorator(func):
        def wrapper(userInput):
            if len(userInput) != n:
                print('Error: Command parameters do not match or is not allowed.')
            else:
                return func(userInput)
        return wrapper
    return length_decorator
# ! ----------------------------------------------------
def receive_messages(sock):
    """Function to receive messages from the server."""
    while True:
        try:
            message = sock.recv(1024).decode()
            print(json.loads(message))
        except:
            sock.close()
            break
# ! ----------------------------------------------------
def type_commands(sock):
    
    while True:
        inp = askCommand()
        newinp = inp.split()

        # * check if it's a command
        command = newinp[0]
        if command[0] != '/':
            print('Error: Invalid command.')
            continue
        print('another loop')

        if command == '/join':
            join(newinp)
        elif command == '/leave':
            leave(newinp)
        elif command == '/register':
            register(newinp)
        elif command == '/all':
            msgAll(newinp)
        elif command == '/msg':
            msg(newinp)
        elif command == '/?':
            help()
        else:
            print('Error: No command was found.')
# ! ----------------------------------------------------
receive_thread = threading.Thread(target=receive_messages, args=(sock,))
send_thread = threading.Thread(target=type_commands, args=(sock,))


# ! ----------------------------------------------------
def sendJSON(dictionary):
    json_str = json.dumps(dictionary)
    sock.sendto(json_str.encode(), serverAddressPort)
    return
# ! ----------------------------------------------------
def askCommand():
    a = input('>>> ')
    return a
# ! ----------------------------------------------------
def welcome():
    print('--------------------------')
    print('|  Message Board System  |')
    print('--------------------------')
    print()
    print('type \'/?\' for list of commands')

@check_args(3)
def join(inp):
    global serverAddressPort, sock
    serverAddressPort= (inp[1], int(inp[2]))
    # print(serverAddressPort, sock)

    try:
        sock.connect(serverAddressPort)
        receive_thread.start()
    except:
        print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
        return

    print('Connection to the Message Board Server is successful!')
    tempDict = {"command":"join"}
    
    sendJSON(tempDict)

@check_args(1)
@connection_req
def leave(inp):
    print('Connection closed. Thank you!')
    tempDict = {"command":"leave"}
    sendJSON(tempDict)

@check_args(2)
@connection_req
def register(inp):
    newHandle = inp[1]
    tempDict = {"command":"register", "handle": newHandle}
    sendJSON(tempDict)
    # success_message = f'Welcome {HANDLE}!'
    return

@check_args(2)
@connection_req
@register_req
def msgAll(inp):
    message = inp[1]
    tempDict = {"command":"all", "message": message}
    sendJSON(tempDict)

@check_args(3)
@connection_req
@register_req
def msg(inp):
    handle, message = inp[1:]
    tempDict = {"command":"msg", "handle":handle, "message":message} 
    sendJSON(tempDict)

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
# ! -----------------CODE STARTS HERE---------------------
welcome()

send_thread.start()
# receive_thread.start()
