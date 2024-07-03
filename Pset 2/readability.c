#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // get text from user
    string text = get_string("Text: ");

    float letters = count_letters(text);
    float words = count_words(text);
    float sentences = count_sentences(text);

    //calculating L and S
    float L = (letters / words) * 100;
    float S = (sentences / words) * 100;

// formula to calculate reading index
    int index = round(0.0588 * L - 0.296 * S - 15.8);


// outputting the grade reading level using calculated index
    if (index >= 16) //for indexes greater than zero
    {
        printf("Grade 16+\n");
    }
    else if (index > 0 && index < 16)
    {
        printf("Grade %i\n", (int)index);
    }
    else // for indexes smaller than zero
    {
        printf("Before Grade 1\n");
    }


}

int count_letters(string text)
//function to count number of letters
{
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i])) //to check if character is alphabetical
        {
            count += 1;
        }
    }
    return count;
}

int count_words(string text)
// function to count number of words
{
    int count = 0;
    for (int i = 0; i <= strlen(text); i++)
    {
        if (text[i] == 32) //to check if character is space
        {
            count += 1;
        }
    }
    return count + 1;
}

int count_sentences(string text)
// function to count number of sentences
{
    int count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 46 || text[i] == 33 || text[i] == 63) //to check if character is either . or ! or ?
        {
            count += 1;
        }
    }
    return count;
}