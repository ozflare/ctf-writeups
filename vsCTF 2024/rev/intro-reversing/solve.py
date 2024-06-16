#!/usr/bin/env python3
from pwn import *
import os

elf = ELF('chall')
mov_edi = elf.sym['main'] + 62

elf.write(mov_edi, p32(0x0))
elf.save('chall_patched')
os.system('chmod +x chall_patched')

p = process('chall_patched')

print(p.recv().decode())
os.system('rm chall_patched')