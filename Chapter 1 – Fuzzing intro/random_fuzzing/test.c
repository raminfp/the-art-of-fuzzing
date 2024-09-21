#include <stdlib.h>
#include <string.h>

int main(int argc, char** argv) {
        /* Create an array with 100 bytes, initialized with 42 */
        char *buf = malloc(100);
        memset(buf, 42, 100);
        /* Read the N-th element, with N being the first command-line argument */
        int index = atoi(argv[1]);
        char val = buf[index];
        /* Clean up memory so we don't leak */
        free(buf);
        return val;
    }
