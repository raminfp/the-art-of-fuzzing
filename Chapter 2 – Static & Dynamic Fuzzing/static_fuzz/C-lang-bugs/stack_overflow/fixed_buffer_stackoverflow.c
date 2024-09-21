// Author : Ramin Farajpour Cami
// usage : gcc -fsanitize=address -g fixed_buffer_stackoverflow.c
// ./a.out


#include <stdlib.h>
#include <stdio.h>


int main(int argc, char **argv) {

   int arr[100];
   int i;
   for (i =0;i <= 101;i++){
  	if (i < sizeof(arr) / sizeof(int))
  	{
      arr[i] = 1;
  	}
    else{
      goto error;
      return 0;
    }
   }
  error:
    printf("%s\n","out of bound");

  return 0;
}
