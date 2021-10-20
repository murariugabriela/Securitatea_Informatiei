#!/usr/bin/env python3

import socket
from server import K_prime
from ECB import *
from CFB import *
import server


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 2729        # The port used by the server
round = 1
decrypted_key = b''
encrypted_key = b''
modeB = AES.MODE_ECB

def decrypt_message_on_chosen_mode(message):
    if modeB == AES.MODE_CFB:
        decrypted_message = cfb_decrypt(message, decrypted_key)
    else:
        decrypted_message = ecb_decrypt(message, decrypted_key)
    return decrypted_message

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(bytes(client_message, "utf-8"))
    while True:
        if round == 1:
            data = s.recv(1024)
            if data == b'CFB':
                modeB = AES.MODE_CFB
        elif round == 0:
            client_message = input("Enter your message: \n")
            s.sendall(bytes(client_message, "utf-8"))
            print('Sent: ', client_message, "\n")
            round = 3
        elif round == -1:
            if modeB == AES.MODE_ECB:
                decrypted_key = ecb_decrypt(encrypted_key, K_prime)
            else:
                decrypted_key = cfb_decrypt(encrypted_key, K_prime)
            round = 4
        else: 
            data = s.recv(1024)
            print('Received', repr(data), "\n")
            if round == -2:
                encrypted_key = data
                s.sendall(b'key_decrypted by B')
                round = 2
            if round == -3:
                #print(modeB, AES.MODE_ECB, AES.MODE_CFB)
                print(decrypt_message_on_chosen_mode(data).decode("utf-8"))
                round = None
        if round is not None:
            round = 1 - round
        else:
            break
        