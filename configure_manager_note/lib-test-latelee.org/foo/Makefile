# A simple Makefile for lib(libxxx.a)
# By Late Lee(http://www.latelee.org)

AR = ar
ARFLAGS = cr

RM = -rm -rf
OBJS = $(patsubst %.c, %.o, $(wildcard *.c))
OUT_LIB_DIR ?= .
LIB = $(OUT_LIB_DIR)/libfoo.a

all: $(LIB)

$(LIB): $(OBJS)
	$(AR) $(ARFLAGS) $@ $(OBJS)

%.o:%.c
	$(CC) $(CFLAGS) -c $<

clean:
	$(RM) $(OBJS) $(LIB) *.bak *~

.PHONY: all clean
