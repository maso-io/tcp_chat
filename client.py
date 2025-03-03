#!/usr/bin/python

from socket import socket, AF_INET, SOCK_STREAM, error
from threading import Thread

#  client should be able to receive and send messages on seperate threads
SOCKET = ('localhost', 12000)
BUFF_SIZE = 1024
client = None

def connect():
    global client
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(SOCKET)
        while True:
            msg = client.recv(BUFF_SIZE).decode()
            print(msg)
            if msg[0] == 'x':
                res = input('')
                client.send(res.encode())
            else:
                # user is connected
                break
    except error as e:
        print(f'Socket Error: {e}')


def receive():
    try:
        while True:
            message = client.recv(BUFF_SIZE).decode()
            print(message)
    except error as e:
        print(f"Socket Error: {e}")

def post():
    while True:
        message = input(":")
        client.send(message.encode())


if __name__ == "__main__":
    connect()

    receive_t = Thread(target=receive)
    receive_t.start()

    post_t = Thread(target=post)
    post_t.start()
