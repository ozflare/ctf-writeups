#!/usr/bin/env python3
import base64

values = [
    0x304e3264684e3359,
    0x7a59334d4f746e5a,
    0x33416a6377396c63,
    0x7a4d3358334d324d,
    0x32467a4e784d6e62,
    0x77596d627838314d,
    0x77457a4e30306d63,
    0x75467a6331396c62,
    0x334d58647139315a,
    0x6b427a59754e7a58,
    0x6a3856496e35574d,
    0x7851474d6a35324d,
    0x664e584d66646d62,
    0x754e7a5830426a62,
    0x78634463354a3359,
    0x3d3d51666834474d,
]

print(base64.b64decode(b''.join([v.to_bytes(8, 'little') for v in values])).decode())
