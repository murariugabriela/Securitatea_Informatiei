#!/usr/bin/env python3
import socket
from server import K_prime
from ECB import *
from CFB import *
import server

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 2729        # The port used by the server
round = 2
crypted_key = b''
decrypted_key = b''
key_sent = False
modeA = AES.MODE_ECB

def encrypt_message_on_chosen_mode(message):
    print("mode", modeA)
    if modeA == AES.MODE_CFB:
        encrypted_message = cfb_encrypt(message, decrypted_key)
    else:
        encrypted_message = ecb_encrypt(message, decrypted_key)
    return encrypted_message

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        if round == 0:
            with open("plaintext.txt", "rb") as f:
                client_message = f.read()
                client_message = encrypt_message_on_chosen_mode(client_message)
                s.sendall(client_message)
                print('Sent: ', client_message)
                round = -3
        elif round == 2:
            client_message = input("Enter encryption mode (ECB or CFB): \n")
            if client_message == 'CFB':
                print(client_message)
                modeA = AES.MODE_CFB
            s.sendall(bytes(client_message, "utf-8"))
        elif round == -1:
            print("mode", modeA)
            crypted_key = s.recv(1024)
            print('Received crypted key', repr(crypted_key), "\n")
            if modeA == AES.MODE_ECB:
                decrypted_key = ecb_decrypt(crypted_key, K_prime)
            else:
                decrypted_key = cfb_decrypt(crypted_key, K_prime)
            round = 0
        else: 
            if round != 4:
                data = s.recv(1024)
                print('Received', repr(data), "\n")
                if crypted_key is not None:
                    print('Sent key', crypted_key)
                    s.sendall(crypted_key)
                    crypted_key = None
                    round = 0
            elif round == 4: 
                round = None
        if round is not None:
            round = 1 - round
        else:
            break