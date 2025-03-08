#!/usr/bin/python

from socket import socket, AF_INET, SOCK_STREAM, error
from threading import Thread
from sys import exit

#  client should be able to receive and send messages on seperate threads
SOCKET = ('localhost', 12000)
BUFF_SIZE = 1024
client = None
username = None
                     
def connect():
    global client
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(SOCKET)
        register_user()
    except error as e:
        print(f'Socket Error: {e}')
        return False
    return True

def register_user():
    global client, username
    try:
        while True:
            msg = client.recv(BUFF_SIZE).decode()
            if not msg:
                # server disconnected
                break
            else:
                if "Enter your username" or "username not available" in msg:
                    print(msg)
                    username = input("")
                    client.send(username.strip().encode())
                else:
                    # user is connected
                    print(msg)
                    break
    except error as e:
        print(f'Error connecting with server, disconnected...')
        print(f'{e}')
        client.close()
        exit(1)
    except KeyboardInterrupt:
        print(f'Client disconnecting from server.')
        client.close()
        exit(0)
    finally:
        print(f'Server disconnected')
        client.close()
        exit(0)

def receive():
    global username
    try:
        while True:
            message = client.recv(BUFF_SIZE).decode()
            if not message:
                # server disconnected
                break
            else:
                if username in message:
                    continue
                print(message)
    except error as e:
        print(f"Receive socket error: {e}")
        client.close() 
        exit(1)
    except KeyboardInterrupt:
        print(f'Disconnecting from server...')
        client.close()
        exit(1)

def post():
    global client
    try:
        while True:
            message = input("")
            if not message.strip():
                continue
            else:
                client.send(message.encode())
    except KeyboardInterrupt:
        print(f'Client disconnecting... ')
        client.close()
        exit(0)



if __name__ == "__main__":
    try:
        if not connect():
            exit(1)
        # start thread to receive messages
        receive_t = Thread(target=receive)
        #receive_t.daemon = True
        receive_t.start()
        # start sending messages on main thread
        post()
    except KeyboardInterrupt:
        print('Client disconnected')
        if client:
            client.close()
        exit(0)
    except error as e:
        print(f'Other error: {e}')
        if client:
            client.close()
        exit(1)
