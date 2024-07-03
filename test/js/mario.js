const readlineSync = require('readline-sync');

var height=0;

while (height > 8 || height < 1)
    {
         height  = readlineSync.question("What's the height? ");
    }

for (i = 1; i <= height; i++)
{
    for (j = 1; j <= height; j++){

        if (j > (height - i))
        {
            process.stdout.write("#");
        }
        else
        {
            process.stdout.write(" ");
        }
        if (j == height)
        {
            process.stdout.write(" ");
            for (let k = 1; k <= i; k++){

                process.stdout.write("#");
            }

        }

    }
    console.log()
}
