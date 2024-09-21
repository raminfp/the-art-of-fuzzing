// Author : Ramin Farajpour Cami
// usage : gcc -fsanitize=address -g buffer_stackoverflow.c
// ./a.out


#include <stdlib.h>
#include <stdio.h>


int main(int argc, char **argv) {

  int arr[100];

 int i;
 for (i =0;i <= 101;i++){
	arr[i] = 1; 
	if (i == 101)
		printf("done!\n");
 }

 return 0;
}
