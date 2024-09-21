// Usage : clang -c -emit-llvm sec_exm.c
// klee sec_exm.bc
// ktest-tool klee-out-0/t

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <klee/klee.h>

int check_string(char *buf, int len) {
	if (buf[0] == 'T' &&
		buf[1] == 'E' &&
		buf[2] == 'S' &&
		buf[3] == 'T'
	) {
	
		assert(0);
	}
	return;
} 

int main() {
  char buf[10];
  klee_make_symbolic(buf, sizeof(buf), "buf");
  check_string(buf, 10)
  return 0;
} 