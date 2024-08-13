#!/usr/bin/env python3
import base64

ciphertext_decoded = base64.b64decode("NkMHEgkxXjV/BlN/ElUKMVZQEzFtGzpsVTgGDw==")
key = "A string of text can be encrypted by applying the bitwise XOR operator to every character using a given key"

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

print(byte_xor(key.encode(), ciphertext_decoded))
