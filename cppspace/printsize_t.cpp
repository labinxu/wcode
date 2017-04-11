#include <stdlib.h>
#include <stdio.h>

typedef struct{
    u_char iphl:4;
} ip;

int main(int argc, char *argv[])
{
    ssize_t y = 1;
    size_t x = 2;
    printf("sizeof %zu\n", sizeof(ip));
    printf("sizeof %zd\n", sizeof(y));
    printf("sizeof %zu\n", sizeof(x));
    return 0;
}
