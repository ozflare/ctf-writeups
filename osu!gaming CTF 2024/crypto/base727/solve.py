#!/usr/bin/env python3
import binascii

def decode_base_727(string):
    decoded_string = ''
    utf = b''

    for c in string:
        if utf == b'' and c < 128:
            decoded_string += chr(c)
        else:
            utf += int.to_bytes(c, 1, 'big')

            if len(utf) == 2:
                decoded_string += utf.decode()
                utf = b''

    decoded_value = 0

    for c in decoded_string:
        decoded_value = decoded_value * 727 + ord(c)

    print(decoded_value)

    flag = ''

    while decoded_value > 0:
        flag = chr(decoded_value % 256) + flag
        decoded_value //= 256
        print(flag)

    return decoded_string

with open('./out.txt', 'r') as f:
    flag = f.read().strip().encode()
    flag = binascii.unhexlify(flag)

    print(decode_base_727(flag))
