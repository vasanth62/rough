
#include <stdio.h> // for puts
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <sys/time.h>

int main (int argc, char** argv)
{
  uint64_t _a;
  uint8_t b;
  uint64_t p, q, r, s;

  p = q = r = s = 5;
  b = 1;

  _a = b;

  printf("%#" PRIx64 "\n", _a);
  printf("%#" PRIx64 "\n", p);
  printf("%#" PRIx64 "\n", q);
  printf("%#" PRIx64 "\n", r);
  printf("%#" PRIx64 "\n", s);
  return 0;
}
