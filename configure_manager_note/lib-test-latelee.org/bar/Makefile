# A simple Makefile for lib(libxxx.a)
# By Late Lee(http://www.latelee.org)

AR = ar
ARFLAGS = cr
LIB = libbar.a
OBJS := bar.o common.o
OUT_LIB_DIR ?= .

all: $(LIB)

$(LIB): $(OBJS)
	$(AR) $(ARFLAGS) -o $(OUT_LIB_DIR)/$@ $(OBJS)

%.o:%.c
	$(CC) $(CFLAGS) -c $<

clean:
	$(RM) $(OBJS) $(OUT_LIB_DIR)/$(LIB) *.bak *~

.PHONY: all clean
