#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
  int a, b;
  char *mem;

  if (argc < 2)
    exit(1);

  a = atoi(argv[1]);
  b = atoi(argv[2]);

  if (a + b > 0) {
	printf("a + b = %d\n", (a + b));
	printf("it's OK\n");
  }
  //else {
//	printf("a + b = %d\n", (a + b));
//	printf("Overflow\n");
 // }

  return 0;
}
