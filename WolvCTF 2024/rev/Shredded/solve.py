#!/usr/bin/env python3
NUM_OF_LINES = 38
NUM_OF_FILES = 33

def get_code_from_shred():
    code = [''] * NUM_OF_LINES

    for i in range(NUM_OF_FILES):
        with open(f'./out/shredFiles/shred{i}.txt') as f:
            for j in range(NUM_OF_LINES):
                code[j] += f.readline()[:-1]

    for i in range(NUM_OF_LINES):
        code[i] = code[i][2:3] \
                + code[i][4:5] \
                + code[i][18:19] \
                + code[i][31:32] \
                + code[i][19:20] \
                + code[i][21:22] \
                + code[i][13:14] \
                + code[i][5:6] \
                + code[i][12:13] \
                + code[i][30:31] \
                + code[i][27:28] \
                + code[i][28:29] \
                + code[i][25:26] \
                + code[i][9:10] \
                + code[i][16:17] \
                + code[i][6:7] \
                + code[i][26:27] \
                + code[i][24:25] \
                + code[i][17:18] \
                + code[i][29:30] \
                + code[i][11:12] \
                + code[i][14:15] \
                + code[i][1:2] \
                + code[i][3:4] \
                + code[i][15:16] \
                + code[i][7:8] \
                + code[i][32:33] \
                + code[i][0:1] \
                + code[i][20:21] \
                + code[i][23:24] \
                + code[i][10:11] \
                + code[i][8:9] \
                + code[i][22:23]

    print('\n'.join(code))

    '''
    #include <stdio.h>
    #include <string.h>

    int main() {
        char flag[] = "REDACTED";
        char inter[51];
        int len = strlen(flag);

        for(int i = 0; i < len; i++) {
            inter[i] = flag[i];
        }

        for(int i = len; i < 50; i++) {
            inter[i] = inter[(i*2)%len];
        }

        inter[50] = '\0';
        char a;

        for(int i = 0; i < 50; i++) {
            a = inter[i];
            inter[i] = inter[((i+7)*15)%50];
            inter[((i+7)*15)%50] = a;
        }

        for(int i = 0; i < 50; i++) {
            a = inter[i];
            inter[i] = inter[((i+3)*7)%50];
            inter[((i+3)*7)%50] = a;
        }

        for (int i = 0; i < 50; i++) {
            inter[i] = inter[i] ^ 0x20;
            inter[i] = inter[i] ^ 0x5;
        }

        for(int i = 0; i < 50; i++) {
            a = inter[i];
            inter[i] = inter[((i+83)*12)%50];
            inter[((i+83)*12)%50] = a;
        }

        for (int i = 0; i < 50; i++) {
            printf("\\x%X ", inter[i]);
        }

        return 0;
    }
    '''

def decode(f):
    new_data = []
    data = []
    raw_data = b''.join(f.readline()[2:].split(b'\x00')).strip().split(b' ')

    for raw in raw_data:
        data.append(int(raw[2:], 16))

    # transposition
    t = [33, 8, 10, 32, 19, 6, 7, 30, 15, 44, 47, 28, 43, 20, 39, 26, 35, 46, 31, 24, 27, 48, 25, 16, 29, 0, 37, 36, 2, 4, 11, 40, 18, 1, 49, 38, 45, 12, 41, 14, 42, 13, 17, 5, 34, 3, 21, 22, 23, 9]

    for i in range(50):
        new_data.append(data[t.index(i)])

    data = new_data

    # xor
    for i in range(50):
        new_data[i] = data[i] ^ 0x25

    data = new_data.copy()
    new_data.clear()

    # transposition
    t = [18, 17, 16, 15, 14, 12, 13, 11, 10, 9, 8, 7, 5, 6, 4, 3, 2, 1, 0, 49, 48, 47, 43, 36, 29, 46, 42, 41, 40, 24, 37, 38, 45, 35, 34, 33, 23, 30, 31, 44, 28, 27, 26, 22, 39, 32, 25, 21, 20, 19]

    for i in range(50):
        new_data.append(data[t.index(i)])

    data = new_data.copy()
    new_data.clear()

    # transposition
    t = [43, 20, 35, 5, 15, 39, 45, 10, 25, 40, 47, 1, 2, 3, 4, 44, 6, 30, 8, 9, 41, 7, 12, 13, 0, 48, 16, 17, 14, 19, 36, 21, 22, 23, 24, 42, 26, 27, 28, 29, 49, 31, 11, 33, 34, 46, 32, 37, 38, 18]

    for i in range(50):
        new_data.append(data[t.index(i)])

    data = new_data.copy()
    new_data.clear()

    flag = ''.join(map(chr, data))
    idx = flag.index('}')
    print(flag[:idx+1])

# get_code_from_shred()
decode(open('./output.txt', 'rb'))
