#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2) //check command-line arguments
    {
        printf("Usage: ./filter IMAGENAME\n");
        return 1;
    }
    FILE *file = fopen(argv[1], "r");
    if (file == NULL) //check for file
    {
        printf("Could not open %s\n", argv[1]);
        return 1;
    }

    BYTE buffer[512]; //create buffer
    FILE *new_image = NULL;
    int images = 0;
    char recovered[8];

    while (fread(buffer, 1, 512, file) == 512) //read file into buffer
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) //check start of image
        {
            if (new_image != NULL) //
            {
                fclose(new_image);
            }
            sprintf(recovered, "%03i.jpg", images); //
            new_image = fopen(recovered, "w");

        }
        if (new_image != NULL)
        {
            fwrite(buffer, 1, 512, new_image); //
        }
    }
    if (new_image != NULL) //
    {
        fclose(new_image);
    }
    fclose(file); //close file
}