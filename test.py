import socket
import threading

def receive_messages(sock):
    """Function to receive messages from the server."""
    while True:
        try:
            message = sock.recv(1024).decode()
            print(message)
        except:
            # An error occurred, likely the server has closed the connection
            print("Connection closed")
            sock.close()
            break

def send_message(sock):
    """Function to send messages to the server."""
    while True:
        message = input()
        sock.sendall(message.encode())

# Get the server address and port
server_address = input("Enter server address: ")
server_port = int(input("Enter server port: "))

# Create a socket and connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_address, server_port))

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(sock,))
receive_thread.start()

# Start a thread to send messages to the server
send_thread = threading.Thread(target=send_message, args=(sock,))
send_thread.start()
