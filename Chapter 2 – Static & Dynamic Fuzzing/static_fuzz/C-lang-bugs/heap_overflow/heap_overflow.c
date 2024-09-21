// Author : Ramin Farajpour Cami
// usage : gcc -fsanitize=address -g heap_overflow.c
// execute : ./a.out
// errors message of ASAN

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc,char** argv){

	char *x = "Ramin";
    	char *y = (char *)malloc(strlen(x));
    	strcpy(y, x);
	printf("Done!\n");
	return 0;
}
