#include <stdlib.h>
#include <stdio.h>


int global_array[100] = {0};

int main(int argc, char **argv) {

 int i;
 for (i =0;i <= 101;i++){
	global_array[i] = 1;
	if (i == 101)
		printf("done!\n");
 }

 return 0;
}
