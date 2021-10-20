#!/usr/bin/env python3
import os
import socket
from _thread import *
import sys
from Crypto.Cipher import AES

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 2729        # Port to listen to
ECB = 'ECB'
CFB = 'CFB'

K_prime = b'&F)J@NcRfUjXn2r5'  # used for K encryption
initialization_vector = b'1234567890123456'

clients = []
key = os.urandom(16)
round = -1
disconnected_clients = 0

class AES_MODE:
    def __init__(self):
        self.mode = AES.MODE_ECB
    def change_mode(self, value):
        self.mode = value
aes_mode = AES_MODE()
def threaded(c):
    global round
    while True:
        # data received from client
        data = c.recv(1024)
        if not data:
            global disconnected_clients
            disconnected_clients += 1
            print('Bye', disconnected_clients)
            if disconnected_clients == 2:
                sys.exit()
            break
        # send back string to client
        if round == -1 and data:
            if data == b'CFB':
                aes_mode.change_mode(AES.MODE_CFB)
                print(aes_mode.mode)
            for client in clients:
                if client != c:
                    client.sendall(data)
            round = 0
        else:
            for client in clients:
                if client != c:
                    client.sendall(data)
    c.close()

def treat_clients():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)
        while True:
            conn, addr = s.accept()
            if len(clients) == 0:
                cipher = AES.new(K_prime, aes_mode.mode)
                conn.sendall(cipher.encrypt(key))
            clients.append(conn)
            print('Connected by', addr)
            start_new_thread(threaded, (conn, ))
        s.close()

if __name__ == '__main__':
    treat_clients()