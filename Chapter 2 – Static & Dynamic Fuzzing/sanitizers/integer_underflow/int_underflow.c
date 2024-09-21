#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{

	char buf[20];
	int i=atoi(argv[1]);
	memcpy(buf,argv[2],i*sizeof(int));
	printf("the number is:%d=%d\n",i,i*sizeof(int));
	printf("the buffer is:%s\n",buf);
}
