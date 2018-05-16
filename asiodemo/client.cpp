#include <deque>
#include <iostream>
#include <boost/array.hpp>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/thread.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <algorithm>
#include "tcp_client.h"

int main(){

    try{
        boost::asio::io_service io_service;
        tcp::endpoint endpoint(boost::asio::ip::address::from_string("127.0.0.1"), 8001);
        tcp_client client(io_service, endpoint);
        boost::thread t(boost::bind(&boost::asio::io_service::run,
                                    &io_service));

        while(client.isActive())
        {
            using namespace std;
            message msg;
            string line;
            std::getline(std::cin, line);
            msg.body_length(line.size());
            memcpy(msg.body(), line.c_str(), msg.body_length());
            msg.encode_header();
            client.send(msg);

        }
        client.close();
        t.join();

    }
    catch (std::exception &e){
        std::cerr<<e.what()<<std::endl;
    }
}
