/**
 * @file   backtrace.c
 * @author Late Lee <latelee@163.com>
 * @date   Wed Feb 23 2011
 * 
 * @brief  
 *         $ gcc backtrace.c main.c -rdynamic -g -Wall
 * 
 * log:
          1.
 */

#include <execinfo.h>	/* backtrace* */
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>	/*O_RDWR*/
#include <unistd.h>	/*close*/
#include <string.h>	/*strlen*/
#include <signal.h>	/*SIGSEGV*/
#include "../configs/backtrace.h"
//#include <backtrace.h>

/* Obtain a backtrace and print it to stdout. */
void print_trace(int sig)
{
	void *array[NEST];
	size_t size;
	char **strings;
	size_t i;

	size = backtrace(array, NEST);
	strings = backtrace_symbols(array, size);
	printf("Obtained %zd stack frames.\n", size);
	for (i = 0; i < size; i++)
		printf("%s\n", strings[i]);
	free(strings);
	
	exit(0);
}

/* Obtain a backtrace and print it to file. */
/* 如创建文件，再次打开则失败，无权限，原因未知。打开已存在文件无此问题
 * fc10中测试无此问题--2.27
 */
void print_trace_fd(int sig)
{
	void *array[NEST];
	size_t size;
	int fd;
	char buf[64];

	fd = open("./bt1.txt", O_CREAT|O_RDWR|O_APPEND);
	if (fd < 0)
	{
		perror("open file failed");
		exit(0);
	}
	size = backtrace(array, NEST);
	sprintf(buf, "Obtained %zd stack frames.\n", size);
	//printf("%s %d\n", buf, strlen(buf));
	write(fd, buf, strlen(buf));
	backtrace_symbols_fd(array, size, fd);
	write(fd, "\n", 1);
	close(fd);
}

/*
 * 在打印符号的同时打印函数名及文件名称和行号
 * 使用addr2line命令打印文件名称和行号，形式：addr2line [option] file addr
 */
void print_trace_file(int sig)
{
	void *addr[NEST];
	char **strings;
	size_t size;
	size_t i;
	int len;
	int ret;
	//FILE *fp;
	/* "-C": this option makes C++ function names readable. */
	char cmd[128] = "addr2line -C -f -e ";
	const char *self = "/proc/self/exe"; /* a link to an exe file, eg. a.out */
	char *path;

	/* SIGSEGV = 11 */
	if (sig == SIGSEGV)
		printf("Segmentation fault\n");
	
	size = backtrace(addr, NEST);
	strings = backtrace_symbols(addr, size);
	printf("Obtained %zd stack frames.\n", size);

	path = cmd + strlen(cmd);
	/* sizeof(cmd)-strlen(self) will be large enough */
	ret = readlink(self, path, sizeof(cmd)-strlen(self));
	if (ret < 0)
	{
		perror("readlink");
		return;
	}
	len = strlen(cmd);	/* keep the addr just after the exe file */
	for (i = 0; i < size; i++)
	{
		printf("\n%s\n", strings[i]);
		/* eg. addr2line -C -f -e /xxx/a.out 0xdeadbeef */
		sprintf(cmd+len, " %p", addr[i]);
		//printf("%s %d\n", cmd, strlen(cmd)); /* print cmd */
		#if 0
		/* 有时不按顺序打印，估计与popen有关，用system没此问题 */
		fp = popen(cmd, "w");
		if (fp == NULL)
		{
			perror("popen");
			exit(0);
		}
		#endif
		#if 1
		ret = system(cmd);	/* execute the cmd */
		if (ret < 0)
		{
			printf("system() error\n");
			return;
		}
		#endif
	
	}
	free(strings);
	//pclose(fp);
	
	exit(0);	/* for <segmentation fault> test */
}