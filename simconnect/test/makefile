SRCS=$(wildcard *.c *.cpp)
OBJS=$(SRCS:.cpp=.o)
CC=g++
INCLUDES=-I/project/nls/3rd_party/include/boost_1_39_0 -I../include
LIBS_PATH=-L/project/nls/3rd_party/VZ/lib_18.0/x86_64
LIBS_PATH+=-L../output

LIBS=-lboost_system-mt -lpthread -lboost_thread-mt -lsimconnect
CXXFLAGS = -g -Wall
SERVER = server
CLIENT = client

all:$(SERVER) $(CLIENT) $(RESULT)
.PHONY : all

$(SERVER): cserver.o 
	gcc $^ -o $@ $(INCLUDES) -L../output -lsimconnect -lpthread

$(CLIENT):client.o 
	$(CC) $^ -o $@ $(INCLUDES) $(LIBS_PATH) $(LIBS)

%.o:%.cpp
	$(CC) -c $< $(INCLUDES) $(CXXFLAGS)

%.o:%.c
	gcc -c $< -I..
clean:
	rm -rf *.o $(SERVER) $(CLIENT)
