// Usage : clang -c -emit-llvm sec_exm.c
// klee --libc=uclibc sec_exm.bc
// ktest-tool klee-out-0/t

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <klee/klee.h>

int check_string(char *buf) {
	if (strcmp(buf, "KLEE_IS_COOL") == 0)
		assert(0)
	return;
} 

int main() {
  char buf[20];
  klee_make_symbolic(buf, sizeof(buf), "buf");
  klee_assume(buf[20 - 1] == '\0');
  check_string(buf, 10)
  return 0;
} 