from server import initialization_vector
from Crypto.Cipher import AES 

def get_xor_result(v1, v2):
    return bytes(a ^ b for (a, b) in zip(v1, v2))

def cfb_encrypt(plaintext, key):
    ciphertext = b''
    iv = initialization_vector
    while plaintext:
        block = plaintext[0:16]
        block = block + b'\0' * (16 - len(block))
        plaintext = plaintext[16:]
        cipher = AES.new(key, AES.MODE_ECB)
        enc_block = cipher.encrypt(iv)
        enc_block = get_xor_result(enc_block, block)
        ciphertext += enc_block
        iv = enc_block
    return ciphertext

def cfb_decrypt(ciphertext, key):
    plaintext = b''
    iv = initialization_vector
    while ciphertext:
        block = ciphertext[0:16]
        ciphertext = ciphertext[16:]
        cipher = AES.new(key, AES.MODE_ECB)
        dec_block = cipher.encrypt(iv)
        dec_block = get_xor_result(dec_block, block)
        plaintext += dec_block
        iv = block
    return plaintext


#with open("plaintext.txt", "rb") as f:
#    print(cfb_decrypt(cfb_encrypt(f.read())))