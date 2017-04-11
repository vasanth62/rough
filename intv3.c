#include <stdio.h>

int X = 10;

int Y = 0;

static int 
add (int a)
{
    return (2*X) + a;
}

int
main (void)
{

    X = add(X++);

    printf("X = %d\n", X);

    Y = Y++;
    printf("Y = %d\n", Y);

    return 0;
}

