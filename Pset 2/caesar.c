#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

bool only_digits(string text);
char rotate(char myChar, int k);

int main(int argc, string argv[])
{
    //Program to run with single command-line argument
    //Every argument should be a digit
    //Convert value of argv[1] to integer
    //User should enter plaintext
    //Rotate each letter in the plaintext
    int k = 0;
    if (argc == 1 || argc > 2) //checking for the number of arguments entered by user
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else if (only_digits(argv[1]) == true) //checking if argument contains digit(s) only
    {
        k = atoi(argv[1]);
        string text = get_string("plaintext: \n");
        for (int i = 0; i < strlen(text); i++)
        {
            text[i] = rotate(text[i], k);
        }

        printf("ciphertext: %s\n", text);
        return 0;
    }

    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }


}

bool only_digits(string text) //function for testing if argument is digit(s) only
{
    for (int i = 0; i < strlen(text); i++)
    {
        if (!(isdigit(text[i])))
        {
            return false;
        }

    }
    return true;
}

char rotate(char myChar, int k) //function to encrypt the plaintext
{
    if (isalpha(myChar)) //check if character is alphabetical
    {
        if (isupper(myChar)) //check if character is uppercase
        {
            char newChar = (((int) myChar - 65) + k) % 26; //encrypting uppercase characters
            newChar = newChar + 65;
            return newChar;
        }
        else
        {
            char newChar = (((int) myChar - 97) + k) % 26; //encrypting lowercase characters
            newChar = newChar + 97;
            return newChar;
        }
    }
    else
    {
        return myChar;
    }
}
