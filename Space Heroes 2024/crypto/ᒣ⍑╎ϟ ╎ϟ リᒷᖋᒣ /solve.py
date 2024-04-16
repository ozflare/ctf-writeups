from Crypto.Cipher import AES
import binascii, os

key = b"3153153153153153"
iv =  os.urandom(16)

ciphertext = open('message.enc', 'rb').read().strip()
cipher = AES.new(key, AES.MODE_CBC, iv)

print(cipher.decrypt(binascii.unhexlify(ciphertext)))
