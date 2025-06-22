import socket
import threading
import os

HOST = '0.0.0.0'
PORT = int(os.environ.get("PORT", 5000))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
clients_lock = threading.Lock()  # To safely edit client list

def broadcast(message, sender):
    with clients_lock:
        for client in clients.copy():
            if client != sender:
                try:
                    client.send(message)
                except:
                    try:
                        client.close()
                    except:
                        pass
                    if client in clients:
                        clients.remove(client)

def handle(client):
    try:
        while True:
            msg = client.recv(1024)
            if not msg:
                break
            broadcast(msg, client)
    except:
        pass
    finally:
        with clients_lock:
            if client in clients:
                clients.remove(client)
        try:
            client.close()
        except:
            pass

def receive():
    print(f"Server started on {HOST}:{PORT}")
    while True:
        client, _ = server.accept()
        with clients_lock:
            clients.append(client)
        threading.Thread(target=handle, args=(client,), daemon=True).start()

receive()
