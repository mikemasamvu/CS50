#include <stdio.h>
#include <stdlib.h>

typedef struct
{
    int *numbers;
    int size;
}
stack;

stack t;
t.numbers = NULL;
t.size = 0;


bool push(int n)
{
    // TODO
    t.numbers = malloc(sizeof(n));
    if (t.numbers == NULL)
    {
        printf("Insufficient memory allocated.\n");
        return false;
    }
    else
    {
        t.numbers[t.size] = n;
        t.size++;
        return true;
    }
}
