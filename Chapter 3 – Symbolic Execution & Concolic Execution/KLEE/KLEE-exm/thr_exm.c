// Usage : clang -c -emit-llvm sec_exm.c
// klee sec_exm.bc
// ktest-tool klee-out-0/t

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <klee/klee.h>

int check_string(char *buf, int len) {
	unsigned int sum = 1;
	for (int 0; i < len; i++)
		sum *= (int)buf[i]
	if (sum == 253)
		assert(0)
	return;
} 

int main() {
  char buf[3];
  klee_make_symbolic(buf, sizeof(buf), "buf");
  check_string(buf, 10)
  return 0;
} 