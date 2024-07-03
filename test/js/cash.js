
const readlineSync = require('readline-sync');


var change = 0;
var count = 0;


while (change <= 0)
    {
      change = readlineSync.question("What's the change? ");
      cents = Math.round(change * 100);
    }

while (cents > 0)
{
    if (cents >= 25)
    {
        cents = cents - 25;
        count++;
    }else
    if (cents >= 10)
    {
        cents = cents - 10;
        count++;
    } else
    if (cents >= 5)
    {
        cents = cents - 5;
        count++;
    }else
    if (cents >= 1)
    {
        cents = cents - 1;
        count++;
    }
}
console.log(count);