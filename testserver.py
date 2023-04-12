import socket
import threading

HOST = '127.0.0.1'
PORT = 8000

clients = []

def handle_client(client_socket, address):
    print(f'New connection from {address}')
    clients.append(client_socket)

    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode()
            print(f'Received from {address}: {data}')

            # Broadcast the message to all other clients
            for client in clients:
                if client != client_socket:
                    client.sendall(f'{address}: {data}'.encode())
        except:
            print(f'Connection from {address} closed')
            clients.remove(client_socket)
            client_socket.close()
            return

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f'Server started on {HOST}:{PORT}')

while True:
    # Wait for a new client connection
    client_socket, address = server_socket.accept()

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
    client_thread.start()
