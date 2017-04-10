# A simple Makefile for lib(libxxx.a)
# By Late Lee(http://www.latelee.org)

AR = ar
ARFLAGS = cr
OUT_LIB_DIR ?= .
LIB = libbt.a
RM = -rm -rf
OBJS := backtrace.o

all: $(LIB)
$(LIB): $(OBJS)
	$(AR) $(ARFLAGS) $(OUT_LIB_DIR)/$@ $(OBJS)
%.o:%.c
	$(CC) $(CFLAGS) -c $<
clean:
	$(RM) $(OBJS) $(OUT_LIB_DIR)/$(LIB) *.bak *~

 .PHONY: all clean
