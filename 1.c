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
  printf( "%x\n", *p); // 78
  printf( "%x\n", *p + 1); // 79
  printf( "%x\n", *( p + 1)); //56

  printf( "%x\n", *(char*)&x); // 78
  printf( "%x\n", *(char*)(&x+1)); // junk

  printf("%d %d\n", f(), f());

  return 0; 
}

