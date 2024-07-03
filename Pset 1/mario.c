#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x;
    do
    {
        x = get_int("Enter pyramid height: ");
    }
    while (x < 1 || x > 8);

    for (int i = 0; i < x; i++)
    {
        for (int j = x - i; j >= 1; j--)
        {
            printf(" ");
        }

        for (int y = 0; y <= i; y++)
        {
            printf("#");
        }
        printf("\n");
    }
}
