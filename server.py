import socket
import threading
import os

HOST = '0.0.0.0'
PORT = int(os.environ.get("PORT", 5000))  # required for Render

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg, client)
        except:
            clients.remove(client)
            client.close()
            break

def receive():
    print(f"Server started on {HOST}:{PORT}")
    while True:
        client, _ = server.accept()
        clients.append(client)
        threading.Thread(target=handle, args=(client,)).start()

receive()
