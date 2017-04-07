#celib Make file
#author chenxin<chenxin619315@gmail.com>
CC = gcc
AR = ar
RM = rm
#flag for develop
CFLAGS = -g -Wall -fPIC
FFLAGS = -O2 -Wall -fPIC
#extra library
EXTRA_LIB =
# share lib file
SH_FILE = libcelib.so
# static lib file
ST_FILE = libcelib.a
TMPDIR=objs

#install path
LIB_DIR = /usr/lib
INCLUDE_DIR = /usr/include/celib

FILES = $(wildcard *.c)
SOURCE=$(FILES:.c=.o)
#OBJS = $(SOURCE)
OBJS :=$(addprefix ./objs/, $(SOURCE))

all: $(SH_FILE) $(ST_FILE)
$(OBJS): | $(TMPDIR)
$(SH_FILE): $(OBJS)
	$(CC) $(CFLAGS) $^ -shared $(EXTRA_LIB) -o $@
$(TMPDIR):
	mkdir $(TMPDIR)
$(ST_FILE): $(OBJS)
	$(AR) cr $@ $^

###$(filter %.o, $(OBJS)):%.c 
#$(OBJS):$(FILES)
#$(filter %.o, $(OBJS)):%.o:%c
$(TMPDIR)/%.o:%.c
	$(CC) $(CFLAGS) -c $< -o $@

-include $(FILES:.c=.d)
%.d: %.c
	@set -e; rm -f $@; \
	$(CC) -M $(CFLAGS) $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$

#clean object
.PHONY: clean
clean:
	find . -name \*.o | xargs rm -f
	find . -name \*.so | xargs rm -f
	find . -name \*.d | xargs rm -f
	$(RM) -f *.a

install:
	@if [ -d $(LIB_DIR) ];then\
			cp $(SH_FILE) $(LIB_DIR);\
			sudo chmod a+x $(LIB_DIR)/$(SH_FILE);\
			sudo chmod og-w $(LIB_DIR)/$(SH_FILE);\
			echo "Congratulation, celib install successfully.";\
		else\
			echo "Fail to install celib, $(LIB_DIR) is not exist.";\
	fi
	@if [ ! -d $(INCLUDE_DIR) ];then\
	    mkdir $(INCLUDE_DIR);\
	fi
	@cp *.h $(INCLUDE_DIR);\
	chmod a+r $(INCLUDE_DIR)/*.h;\
	chmod a+x $(INCLUDE_DIR)/*.h;
