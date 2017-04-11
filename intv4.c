#include<stdio.h>


void
abc (int *arr)
{

    char *x = "Hello";

//    printf("sizeof int %zu", sizeof(int));
    printf("Size of array - %zu", sizeof(arr));
    printf("\n");
    printf("Size of string - %zu", sizeof(x));
    printf("\n");
}

int main()
{
    int arr[5] = {6,7,8,9,10};


    abc(arr);

}

