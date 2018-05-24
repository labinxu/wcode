#ifndef SIMCONNECT_H
#define SIMCONNECT_H

#ifdef __cplusplus
extern "C"{
    typedef void (*MsgHandler)(const char*, int);

    int regist_in_message_handler(MsgHandler handler);
    int regist_out_message_handler(MsgHandler handler);
    void start_server(const char*ip, int port,
                      const char* peerip,
                      int peerport,
                      MsgHandler ih, MsgHandler oh);
}
#endif

#endif
