SRCS = $(wildcard *.cpp ../lib/*.cpp)
OBJS = $(SRCS:.cpp = .o)
CC = g++
CCFLAGS = -g -Wall -std=c++14 -O0
.PHONY:all clean
# all:$(OUTPUT)
all:
        for f in $(SRCS); do \
        $(CC) -o `echo $$f | sed s/.cpp/.exe/g` $$f $(CCFLAGS);\
        done;

clean:
        rm -rf *.exe *.o
