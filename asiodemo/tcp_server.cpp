#include <cstddef>
#include <ctime>
#include <deque>
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
#include "tcp_server.hpp"
typedef std::deque<message> message_queue;

using namespace boost::asio;
using boost::asio::ip::tcp;


int main( int argc, char* argv[]){
    try{
        boost::asio::io_service io_service;
        tcp_server server(io_service, "127.0.0.1", 8001);
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
