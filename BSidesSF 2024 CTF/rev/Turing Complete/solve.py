#!/usr/bin/env python3
from pwn import *

r = remote('turing-complete-8e4bdad0.challenges.bsidessf.net', 1954)
flag = ''

r.recvline()

for i in range(0x28):
    r.sendline(b'0')
    r.sendline(b'0')

for i in range(0x12):
    r.sendline(b'1')
    r.sendline(b'0')

    r.sendline(b'0')
    r.sendline(b'0')

    flag += chr(int(r.recv(8).decode(), 2))

print(flag)
