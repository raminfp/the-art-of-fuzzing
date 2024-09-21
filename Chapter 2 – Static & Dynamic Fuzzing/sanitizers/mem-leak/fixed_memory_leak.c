// Author : Ramin Farajpour Cami
// usage : gcc -fsanitize=address -g fixed_memory_leak.c
// execute : ./a.out


#include <stdlib.h>
#include <stdio.h>

void test(int *p);

int main(int argc, char **argv) {

  int *ptr;
  ptr = malloc(sizeof(ptr));
  *ptr = 0;
  test(ptr);
  return 0;
}

void test(int *p){
    int *a = p;
    printf("%d\n", *p);
    free(p);
}
