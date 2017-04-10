#include <stdio.h>

#include <backtrace.h>
#include <foo.h>
#include <bar.h>

int main(void)
{
	printf("hello from %s()\n\n", __func__);
	hello_foo();
	hello_bar();
	
	print_trace(111);
	return 0;
}