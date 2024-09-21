#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  char buffer[6] = {0};
  int i;
  int *null = 0;

  read(0, buffer, 6);
  if (buffer[0] == '7' && buffer[1] == '/' && buffer[2] == '4'
      && buffer[3] == '2' && buffer[4] == 'a' && buffer[5] == '8') {
    i = *null;
  }

  puts("No problem");
}