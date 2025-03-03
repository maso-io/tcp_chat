#!/usr/bin/python

from socket import socket, AF_INET, SOCK_STREAM, error
from threading import Thread

SOCKET = ('localhost', 12000)
BUFF_SIZE = 1024
server = None
users = {}

def server_start():
    global server
    try:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind(SOCKET)
        server.listen(5)
        print("Server succecfully started!")
    except error:
        print(f"Socket Error: {error}")
        raise ConnectionError("Server conection failed")

def accept():
    while True:
        try:
            client, addr = server.accept()
            print(f'{addr} connected with server!')

            # Handle some registration
            register_user_thread = Thread(target=register_user, args=(client,))
            register_user_thread.start()

        except error as e:
            print(f'Connection accept error: {e}')

def register_user(client):
    global users
    try:
        msg = "Enter your username: "
        client.send(msg.encode())
        username = client.recv(BUFF_SIZE)
        if username in users:
            msg = "username not available, try again".encode()
            client.send(msg)
        else:
            msg = f"{username} just joined the chat!"
            users[username] = client
            receive_thread = Thread(target=receive, args=(username, client,))
            receive_thread.start()
            broadcast(msg)
    except error as e:
        print(f'Client registration error: {e}')

def broadcast(msg):
    for client in users.values():
        try:
            client.send(msg.encode())
        except error as e:
            msg = f'Error: {e}\nMessage: {msg} could not be sent to {client}'
            pass

def receive(username, client):
    while True:
        try:
            msg = client.recv(BUFF_SIZE).decode().strip()
            if not msg:
                # client disconnected
                break
            msg = f'{username}: {msg}'
            broadcast(msg)
        except error as e:
            print(f'[{username}] Receive error: {e}')
            break

    if username in users:
        del users[username]
        msg = f'{username} has left the chat'
        broadcast(msg)
    client.close()

if __name__ == "__main__":
    server_start()
    accept_thread = Thread(target=accept)
    accept_thread.daemon = True
    accept_thread.start()

    try:
        accept_thread.join()
    except KeyboardInterrupt:
        print("Server shutting down")
        if server:
            server.close()
