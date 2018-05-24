#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include "../simconnect.h"
typedef void (*MsgHandler)(const char* , int);
extern void regist_in_message_handler(MsgHandler handler);
extern void regist_out_message_handler(MsgHandler handler);
extern void start_server(const char*ip, int port, const char* peerip, int peerport, MsgHandler ih, MsgHandler oh);

void handle_in_message(const char*msg, int length){
  printf("hanlder =====printf from caller %s",msg);
}
int start(void *argv){

  start_server("127.0.0.1",8000, "127.0.0.1", 0, handle_in_message, handle_in_message);

  /* MsgHandler handler = handle_in_message; */
  /* printf("regist in handler"); */
  /* regist_in_message_handler(handler); */
  /* regist_out_message_handler(handler); */
  while(1){
    printf("serviceing");
    sleep(10);
  }
}
int main(){
  pthread_t threadid;
  pthread_create(&threadid,NULL, start, NULL);
  

}
