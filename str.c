#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#define SEL_LEN_SHIFT "sel_len"

int main ()
{
  uint64_t a;

  a = (uint64_t)(1<<34);
  printf("Number %#" PRIx64 "\n", a);

  char *to_check = "sel_len_shift";

  if (!strncmp(to_check, SEL_LEN_SHIFT, strlen(SEL_LEN_SHIFT) + 1)) {
    printf("MATCH\n");
  } else {
    printf("NO MATCH\n");
  }
  return 0;
}
