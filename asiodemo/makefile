SRCS=$(wildcard *.c *.cpp)
OBJS=$(SRCS:.cpp=.o)
CC=g++
INCLUDES=-I/project/nls/3rd_party/include/boost_1_39_0
LIBS_PATH=-L/project/nls/3rd_party/VZ/lib_18.0/x86_64
LIBS=-lboost_system-mt -lpthread -lboost_thread-mt
CXXFLAGS = -g -Wall
SERVER = server
CLIENT = client
RESULT = bin

all:$(SERVER) $(CLIENT) $(RESULT)
.PHONY : all

$(SERVER): tcp_server.o
	$(CC) $^ -o $@ $(INCLUDES) $(LIBS_PATH) $(LIBS)

$(CLIENT):tcp_client.o
	$(CC) $^ -o $@ $(INCLUDES) $(LIBS_PATH) $(LIBS)

$(RESULT):
	mv $(SERVER) $(CLIENT) $(RESULT)

%.o:%.cpp
	$(CC) -c $< $(INCLUDES) $(CXXFLAGS)

clean:
	rm -rf *.o $(SERVER) $(CLIENT)
