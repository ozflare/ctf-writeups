#!/usr/bin/env python3
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import unpad
import base64

ciphertext = base64.b64decode("OIkZTMehxXAvICdQSusoDP6Hn56nDiwfGxt7w/Oia4oxWJE3NVByYnOMbqTuhXKcgg50DmVpudg=")
key = base64.b64decode("ZW5jcnlwdG9yZW5jcnlwdG9y")

cipher = Blowfish.new(key, Blowfish.MODE_ECB)

print(unpad(cipher.decrypt(ciphertext), Blowfish.block_size).decode())
