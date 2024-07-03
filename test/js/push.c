#include <stdio.h>

int full()
{
    if (s.size == CAPACITY)
    {
        return true;
    }
    else
    {
        return false;
    }

}

bool push(int n)
{
    // TODO
    if (!full(s))
    {
        s.numbers[s.size] = n;
        s.size++;
        return true;
    }
    else
    {
        printf("Stack is full.\n");
        return false;
    }
}


