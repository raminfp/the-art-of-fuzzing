// Author : Konstantin Serebryany, Google
// Usage : gcc -g -fsanitize=address stack_use_after_return.c
// again usage : ASAN_OPTIONS=detect_stack_use_after_return=1 ./a.out
// erros message ASAN

int *g;

void LeakLocal() {

 	int local;
	g = &local;
}

int main() {

 	LeakLocal();
 	return *g;
}

