#include "simconnect.h"
#include "tcp_server.h"
#include <iostream>
static tcp_server *server = NULL;

void start_server(const char*hostip="127.0.0.1", int hostport=8000,
                  const char* peerip=NULL, int peerport=0,
                  MsgHandler outmsghandler=NULL,
                  MsgHandler inmsghandler=NULL){

    boost::asio::io_service ioservice;
    if(server == NULL){
        tcp_server::address hostaddress = boost::make_tuple(hostip, hostport);
        tcp_server::address peeraddress = boost::make_tuple(peerip, peerport);
        server = new tcp_server(ioservice, hostaddress, peeraddress);
        server->outmessage_handler(outmsghandler);
        server->inmessage_handler(inmsghandler);
        boost::thread t(boost::bind(&boost::asio::io_service::run, &ioservice));
        t.join();
    }
}

int regist_in_message_handler(MsgHandler handler){
    if (server == NULL){
        std::cout<<"Server not running"<<std::endl;
        return 1;
    }
    std::cout<<"regist in message handler"<<std::endl;
    server->inmessage_handler(handler);
    return 0;
}

int regist_out_message_handler(MsgHandler handler){
    if (server == NULL){
        std::cout<<"Server not running"<<std::endl;
        return 1;
    }
    std::cout<<"regist out message handler"<<std::endl;
    server->outmessage_handler(handler);
    return 0;
}

