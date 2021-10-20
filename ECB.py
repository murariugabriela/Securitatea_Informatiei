from Crypto.Cipher import AES

def ecb_encrypt(plaintext, key):
    ciphertext = b''
    while plaintext:
        block = plaintext[0:16]
        block = block + b'\0' * (16 - len(block))  # padding if necessary
        plaintext = plaintext[16:]
        cipher = AES.new(key, AES.MODE_ECB)
        enc_block = cipher.encrypt(block)
        ciphertext += enc_block
    return ciphertext

def ecb_decrypt(ciphertext, key):
    plaintext = b''
    while ciphertext:
        block = ciphertext[0:16]
        ciphertext = ciphertext[16:]
        cipher = AES.new(key, AES.MODE_ECB)
        dec_block = cipher.decrypt(block)
        plaintext += dec_block
    return plaintext

#with open("plaintext.txt", "rb") as f:
#    print(ecb_decrypt(ecb_encrypt(f.read())))