#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

int foo(char *arr, int t1) {
	int i = 0;
	if (arr[i++] == 'c') return 0;
	if (arr[i++] == 'd') return 1;
	if (arr[i++] == 'c') return 2;
	if (arr[i++] == 'c') return 3;
	if (arr[i++] == 's') return 4;
	if (arr[i++] == 'b') return 5;
	if (arr[i++] == 's') return 6;
	if (arr[i++] == 'g') return 7;
	if (*(int *)arr != 0xdeadbeef) return 0;

	return (int)(20 / t1);

}
int main(int argc, char* argv[]) {


	FILE *f = fopen(argv[1], "rb");

	fseek(f, 0, SEEK_END);
	long fsize = ftell(f);

	fseek(f, 0, SEEK_SET);
	char *string = malloc(fsize + 1);
	fread(string, 1, fsize, f);
	fclose(f);

	int retval = foo(string, argc-2);

	free(string);

	return retval;

}
