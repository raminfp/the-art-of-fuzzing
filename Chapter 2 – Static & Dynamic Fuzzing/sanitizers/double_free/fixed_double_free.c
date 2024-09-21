// Author : Ramin Farajpour Cami
// usage : gcc -fsanitize=address -g fixed_double_free.c
// execute : ./a.out
//

#include <stdlib.h>
#include <stdio.h>


int main(int argc, char **argv) {
  int *ptr;
  ptr = (int *)malloc(sizeof(ptr));
  *ptr = 0;
  free(ptr);
  return 0;
}
