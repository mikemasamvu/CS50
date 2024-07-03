const readlineSync = require('readline-sync');

let text = readlineSync.question("Type the text ");

var characters = text.length
var letters = 0;
var sentences = 0

var words = 1;

for (i = 0; i <= characters; i++)
{
    if (isAlpha((text[i])))
    {
        letters++;
    }
    else if (text[i] == " ")
    {
        words++;
    }
    else if (text[i] == "." || text[i] == "!" || text[i] == "?")
    {
        sentences++;
    }
}

let grade = Math.round(0.0588 * ((letters / words) * 100) - 0.296 * ((sentences / words) * 100) - 15.8)

if (grade >= 16)
{
    console.log("Grade 16+");
}
else if (grade < 1)
{
    console.log("Before Grade 1")
}
else
{
    console.log("Grade, " + grade)
}


function isAlpha(char) {
    return (/[a-zA-Z]/).test(char)
  }
