#include <stdio.h>


int isempty()
{

   if (s.size == 0)
   {
    return true;
   }
   else
   {
    return false;
   }

}


bool pop(int *n)
{
    // TODO
   if (!isempty())
   {
      n = s.numbers[s.size];
      s.size--;
      print(n);
      return true;
   }
   else
   {
      printf("Stack is empty.\n");
      return false;
   }

}
