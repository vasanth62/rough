#include <stdio.h>

int main (void)
{
    int a, b, c, d, e;

    a = 5;
    b = a++ + a;

    a = 5;
    c = a + a++;

    a = 5;
    d = (a++ == 5) ? 1:a++;

    a = 5;
    e = (a++ == 5) ? a++:1;

    printf("a = %d\n", a);
    printf("b = %d\n", b);
    printf("c = %d\n", c);
    printf("d = %d\n", d);
    printf("e = %d\n", e);

    return 0;
}

