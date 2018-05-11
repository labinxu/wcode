SRCS=$(wildcard *.c *.cpp)
OBJS=$(SRCS:.cpp=.o)
CC=g++
INCLUDES=-I/project/nls/3rd_party/include/boost_1_39_0
LIBS_PATH=-L/project/nls/3rd_party/VZ/lib_18.0/x86_64
LIBS=-lboost_system-mt -lpthread
#CXXFLAGS = -g -Wall
SERVER=server

all:$(SERVER)
objs:
	echo $(OBJS)

%.o:%.cpp
	$(CC) -c $< $(INCLUDES) $(CXXFLAGS)

$(SERVER):$(OBJS)
	$(CC) $^ -o $@ $(INCLUDES) $(LIBS_PATH) $(LIBS)

clean:
	rm -rf *.o $(TARGET)
