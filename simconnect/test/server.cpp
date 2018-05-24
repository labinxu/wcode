#include <cstddef>
#include <ctime>
#include <string>
#include <iostream>
#include <iterator>
#include <algorithm>
#include <vector>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/thread.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>
#include "message.hpp"
#include "tcp_server.h"
#include "cmdline.h"


using namespace boost::asio;
using boost::asio::ip::tcp;
using namespace std;

int main(int argc, char* argv[]){
    cmdline::parser parser;
    parser.add<std::string>("host", 'h', "host ip",false,"127.0.0.1");
    parser.add<int>("port",'p',"port number", false, 8001);

    parser.add<std::string>("peer", 's', "peer host ip",false, "127.0.0.1");
    parser.add<int>("peerport",'P',"peer host port", false, 0);

    parser.parse_check(argc, argv);

    std::string hostip = parser.get<string>("host");
    int  hostport = parser.get<int>("port");

    std::cout<<"listening on:"<<hostip<<":"<<hostport<<std::endl;
    tcp_server::address hostaddress = boost::make_tuple(hostip, hostport);
    std::string peer_host = parser.get<string>("peer");
    int peer_port = parser.get<int>("peerport");

    tcp_server::address peer_server = boost::make_tuple(peer_host, peer_port);
    try{
        boost::asio::io_service io_service;
        tcp_server server(io_service, hostaddress, peer_server);

        boost::thread t(boost::bind(&boost::asio::io_service::run, &io_service));
        while(true)
        {
            using namespace std;
            message msg;
            string line;
            std::getline(std::cin, line);
            msg.body_length(line.size());
            memcpy(msg.body(), line.c_str(), msg.body_length());
            msg.encode_header();
            server.send(msg);
        }

        t.join();
 
    }
    catch(std::exception &e){
        std::cerr<<e.what()<<std::endl;
    }

    return 0;
}
