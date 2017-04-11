#include <stdio.h>
#include <string.h>

int f(void) {
  static int a = 4;
  a += 1;
  return a;
}

int main() { 
  int x = 0x12345678;
  char *p = (char *)&x;
  printf( "%x\n", *p);
  printf( "%x\n", *p + 1);
  printf( "%x\n", *( p + 1));

  printf( "%x\n", *(char*)&x);
  printf( "%x\n", *(char*)(&x+1));

  printf("%d %d\n", f(), f());

  return 0; 
}

