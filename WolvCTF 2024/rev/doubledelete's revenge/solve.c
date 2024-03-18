#include <stdio.h>

#define ROR(x,y) ((unsigned)(x) >> (y) | (unsigned)(x) << 32 - (y))

int main(int argc, const char **argv, const char **envp) {
  FILE *stream;
  FILE *s;
  int i;
  int ptr[12];
  
  if (argc == 3) {
    stream = fopen(argv[1], "r");

    fread(ptr, 1, 0x30, stream);

    for (i = 0; i < 12; ++i)
      ptr[i] = ROR(ptr[i], 13);

    s = fopen(argv[2], "wb");

    fwrite(ptr, 1, 0x30, s);
  } else {
    printf("[wolphvlog] usage: %s <infile> <ofile>", *argv);
  }

  return 0;
}