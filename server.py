#!/usr/bin/python

from socket import socket, AF_INET, SOCK_STREAM, error
from threading import Thread

SOCKET = ('localhost', 12000)
BUFF_SIZE = 1024
#server = None
users = {}
user =  None

#def server_start():
#    try:
server = socket(AF_INET, SOCK_STREAM)
server.bind(SOCKET)

server.listen(5)
print("Server succecfully started!")
#    except error:
print(f"Socket Error: {error}")
 #       raise ConnectionError("Server conection failed")
#    return server

def accept():
    while True:
        try:
            client, addr = server.accept()
            print(f'{addr} connected with server!')
            while True:
                msg = "x Enter your username: "
                client.send(msg.encode())
                username = client.recv(BUFF_SIZE)
                if users[username]:
                    msg = "Username not availble, try again".encode()
                    client.send(msg)
                else:
                    msg = f"{username} just joined the chat!"
                    users[username] = client
                    broadcast(msg)
                    return username
        except error as e:
            print(f'Client connection error: {e}')
            return

def broadcast(msg):
    for client in users.values():
        client.send(msg.encode())

def receive(user):
    client = users[user]
    while True:
        try:
            msg = client.recv(BUFF_SIZE)
            client.broadcast(msg)
        except error as e:
            print(f'[{user}]Receive error: {e}')
            break

if __name__ == "__main__":
#    server = server_start()
    
    accept_t = Thread(target=accept)
    user = accept_t.start()

    receive_t = Thread(target=receive, args=(user))
    receive_t.start()
