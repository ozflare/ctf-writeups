#!/usr/bin/env python3
import os

images = []

os.system('binwalk -e --run-as=root A_Real_Space_Hero.jpg')

for i in range(400):
    images.append(f'_A_Real_Space_Hero.jpg.extracted/secrets/piece_{i}.png')

    if i % 20 == 19:
        os.system(f'convert {" ".join(images)} +append {i // 20}.png')
        images.clear()

images.clear()

for i in range(20):
    images.append(f'{i}.png')

os.system(f'convert {" ".join(images)} -append result.png')
os.system('zbarimg result.png')
os.system('rm -rf _A_Real_Space_Hero.jpg.extracted')
os.system('rm *.png')
