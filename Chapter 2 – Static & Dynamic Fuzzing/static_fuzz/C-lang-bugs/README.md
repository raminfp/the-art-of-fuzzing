# Address Sanitizer C Language


## Type Vulnerabilities :

1- Heap Overflow<br />
2- Stack buffer Overflow<br />
3- Memory leak<br />
4- Integer Overflow<br />
5- Integer Underoverflow<br />
6- Use After Free<br />
7- Use After return<br />
8- Type Confusion<br />
9- Uninitialized memory access<br />
10- Global Bufferoverflow<br />
11- Double Free<br />

<br />
Usage ex: 

	[root@raminfp]# gcc -fsanitize=address -g double_free.c
	[root@raminfp]# ./a.out
