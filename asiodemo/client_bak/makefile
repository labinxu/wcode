SRCS=$(wildcard *.c *.cpp)
OBJS=$(SRCS:.cpp=.o)
CC=g++
INCLUDES=-I/project/nls/3rd_party/include/boost_1_39_0
LIBS_PATH=-L/project/nls/3rd_party/VZ/lib_18.0/x86_64
LIBS=-lboost_system-mt -lpthread -lboost_thread-mt
CXXFLAGS = -g -Wall
CLIENT=tcp_client
all:$(CLIENT)

$(CLIENT):$(OBJS)
	$(CC) $^ -o $@ $(INCLUDES) $(LIBS_PATH) $(LIBS)

$(OBJS):$(SRCS)
	$(CC) -c $< $(INCLUDES) $(CXXFLAGS)

clean:
	rm -rf *.o $(TARGET)

.PHONY:clean
