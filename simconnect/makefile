SRCS=$(wildcard *.c *.cpp)
OBJS=$(SRCS:.cpp=.o)
CC=g++
INCLUDES=-I/project/nls/3rd_party/include/boost_1_39_0
LIBS_PATH=-L/project/nls/3rd_party/VZ/lib_18.0/x86_64
LIBS=-lboost_system-mt -lpthread -lboost_thread-mt
CXXFLAGS = -g -Wall
SHARED_LIB = libsimconnect.so
all:$(SHARED_LIB)
.PHONY : all

%.o:%.cpp
	rm -f $@
	$(CC) -fpic -c $< -o $@ $(INCLUDES) $(CXXFLAGS) 

$(SHARED_LIB): $(OBJS)
	mkdir -p output
	rm -rf output/$@
	$(CC) -shared -fPIC -o output/$@ $(OBJS) $(LIBS_PATH) $(LIBS)
clean:
	rm -rf *.o output
