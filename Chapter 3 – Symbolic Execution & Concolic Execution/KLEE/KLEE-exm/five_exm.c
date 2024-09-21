// Usage : clang -c -emit-llvm sec_exm.c
// klee --libc=uclibc sec_exm.bc
// ktest-tool klee-out-0/t

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <time.h>
#include <klee/klee.h>

int get_value_based_on_time() {
	time_t rawtime;
	struct tm timeinfo;
	
	time (&rawtime);
	timeinfo = *(localtime (&rawtime));
	printf("Current local time and date: %s", asctime(&timeinfo));
	klee_make_symbolic(&timeinfo, sizeof(strcut tm), "timeinfo");
	if (timeinfo.tm_min == 12)
		assert(0)
	return;
} 

int main() {
  return get_value_based_on_time();
} 