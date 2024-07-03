#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Ask for user string
    string name = get_string("What is your name? ");
    //Prints user string
    printf("hello, %s\n", name);
}