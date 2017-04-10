#################################################################
# A simple Makefile
# By labinxu
##################################################################
export CC=gcc
export CFLAGS = -Wall
export DEBUG = y

ifeq ($(DEBUG), y)
CFLAGS += -g
else
CFLAGS += -O2
endif

SUBDIRS := bar bt foo
INC_DIR = ./configs/
# the ouput dir
ROOT_DIR = $(shell pwd)
OUT_DIR := $(ROOT_DIR)/out/bin
OUT_LIB_DIR := $(ROOT_DIR)/out/lib
export OUT_LIB_DIR

# $(warning $(OUT_LIB_DIR))
# make the libs like out/lib/libfoo.a 
LIBS := libbt.a libfoo.a libbar.a
LIBS := $(addprefix $(OUT_LIB_DIR)/, $(LIBS))

LDFLAGS = $(LIBS)
export RM = -rm -rf

SOURCE = $(wildcard *.c)
OBJS = $(SOURCE:.c=.o)

target = $(OUT_DIR)/a.out
MAKE = make

#all: clean $(target)
all: $(target)

# make output dir
$(target):|$(OUT_DIR)
		$(OUT_DIR):
	mkdir -p $(OUT_DIR);mkdir -p $(OUT_LIB_DIR)

%.o:%.c
	$(CC) $(CFLAGS) -c $< -I$(INC_DIR)

$(target): $(OBJS)
	for dir in $(SUBDIRS); \
	do $(MAKE) -C $$dir all || exit 1; \
	done
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

clean:
	@for dir in $(SUBDIRS); do make -C $$dir clean|| exit 1; done
	$(RM) $(OBJS) $(target) *.bak *~

.PHONY: all clean
