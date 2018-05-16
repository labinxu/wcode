#include <cstddef>
#include <ctime>
#include <queue>
#include <string>
#include <iostream>
#include <iterator>
#include <algorithm>
#include <vector>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/tuple/tuple.hpp>
#include <boost/thread.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>
#include "tcp_connetion.hpp"
#include "tcp_client.h"
#include "message.hpp"

//typedef std::queue<message::pointer> message_queue;

using namespace boost::asio;
using boost::asio::ip::tcp;


class tcp_server{
public:
    typedef boost::tuple<std::string, int> address;
    typedef boost::lock_guard<boost::mutex> lock_guard;

public:
    tcp_server(boost::asio::io_service &io_service,
               const address &hostaddress,
               const address &peer_server=boost::make_tuple("", 0))
        :io_service_(io_service),
         acceptor_(io_service,
                   tcp::endpoint(ip::address::from_string(hostaddress.get<0>().c_str()),
                                 hostaddress.get<1>())),
         peer_server_(peer_server){

        tcp_connection::pointer new_connection(new tcp_connection(io_service_, this));
        acceptor_.async_accept(new_connection->socket(),
                               boost::bind(&tcp_server::handle_accept,
                                           this,
                                           new_connection,
                                           placeholders::error));

        if(boost::get<1>(peer_server_)!=0){
            tcp::endpoint endpoint(ip::address::from_string(boost::get<0>(peer_server_).c_str()),
                                   boost::get<1>(peer_server_));
            tcp_client::pointer c(new tcp_client(io_service_, endpoint));
            client_ = c;
        }
    }

    void handle_accept(tcp_connection::pointer new_connection,
                       const boost::system::error_code &ec){

        std::cout<<"new connection"<<std::endl;
        if (!ec){
            connections_.push_back(new_connection);
            new_connection->start();

            tcp_connection::pointer new_connection(new tcp_connection (io_service_, this));
            acceptor_.async_accept(new_connection->socket(),
                                   boost::bind(&tcp_server::handle_accept,
                                               this,
                                               new_connection,
                                               placeholders::error));
        }
    }

    void send(const message &msg){
        std::vector<tcp_connection::pointer>::iterator it = connections_.begin();
        for (;it != connections_.end(); ++it){
            (*it)->send(msg);
        }
    }

    // message::pointer get_message(){
    //     lock_guard lkgd(mutex_in_msg_);
    //     if (!in_messages_.empty()){
    //         message::pointer msg = in_messages_.front();
    //         in_messages_.pop();
    //         return msg;
    //     }
    //     else{
    //         message::pointer p;
    //         reurn p;
    //     }
    // }

    void append_message(message::pointer msg){
        lock_guard lkgd(mutex_out_msg_);
        //out_messages_.push(msg);
    }

private:
    std::vector<tcp_connection::pointer> connections_;
    boost::asio::io_service &io_service_;
    boost::asio::ip::tcp::acceptor acceptor_;
    address peer_server_;
    message_queue in_messages_;
    message_queue out_messages_;
    boost::mutex mutex_in_msg_;
    boost::mutex mutex_out_msg_;
    tcp_client::pointer client_;
};

