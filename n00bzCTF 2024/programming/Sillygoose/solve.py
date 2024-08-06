#!/usr/bin/env python3
from pwn import *

def search(r, min, max):
    v = (min + max) // 2

    r.sendline(str(v).encode())

    result = r.recv()

    if b'large' in result:
        search(r, min, v - 1)
    elif b'small' in result:
        search(r, v + 1, max)
    else:
        print(result)

r = remote('24.199.110.35', 41199)

search(r, 0, pow(10, 100))
