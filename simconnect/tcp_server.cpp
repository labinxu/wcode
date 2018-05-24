#include <cstddef>
#include <ctime>
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
#include "tcp_client.h"
#include "tcp_server.h"
#include "message.hpp"

//typedef std::queue<message::pointer> message_queue;

using namespace boost::asio;
using boost::asio::ip::tcp;
tcp_server::tcp_server(boost::asio::io_service &io_service,
                       const address &hostaddress,
                       const address &peer_server)
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
    std::string peer_ip = boost::get<0>(peer_server_);
    int peer_port = boost::get<1>(peer_server_);
    if(boost::get<1>(peer_server_) != 0){
        std::cout<<"peer server:"<<peer_ip<<":"<<peer_port <<std::endl;
        std::cout<<"Peer Server Enabled"<<std::endl;
        tcp::endpoint endpoint(ip::address::from_string(boost::get<0>(peer_server_).c_str()),
                               boost::get<1>(peer_server_));
        tcp_client::pointer c(new tcp_client(io_service_, endpoint, this));
        client_ = c;
    }
    else{
        std::cout<<"Peer Server Disabled"<<std::endl;
    }

    boost::thread handle_out_message_t(boost::bind(&tcp_server::handle_out_message, this));
    boost::thread handle_in_message_t(boost::bind(&tcp_server::handle_in_message, this));
    // handle_in_message_t.join();
    // handle_out_message_t.join();
    
}
void tcp_server::inmessage_handler(MsgHandler handler){
        inmessage_handler_=handler;
}
void tcp_server::outmessage_handler(MsgHandler handler){
        outmessage_handler_ = handler;
}
void tcp_server::handle_out_message(){
    
    while(true){
        //
        std::cout<<"loop out message"<<std::endl;
        message::pointer msg = pick_out_message();
        std::cout<<"handle message: "<<msg->body()<<std::endl;
        if (outmessage_handler_ != NULL){
          outmessage_handler_(msg->body(), msg->body_length());
        }
        else{
            std::cout<<"handler null"<<std::endl;
        }
        handle_out_message(msg);
        boost::this_thread::sleep(boost::posix_time::seconds(1));
    }
}

void tcp_server::handle_in_message(){
    //
    while(true){
        //
        std::cout<<"loop in message "<<std::endl;

        message::pointer msg = pick_in_message();
        std::cout<<"handle in message"<<msg->body()<<std::endl;
        if (inmessage_handler_){
            (*inmessage_handler_)(msg->body(), msg->body_length());
        }
        else{
            std::cout<<"handler null"<<std::endl;
        }
        handle_in_message(msg);
        boost::this_thread::sleep(boost::posix_time::seconds(1));
    }
}

void tcp_server::handle_accept(tcp_connection::pointer new_connection,
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

void tcp_server::send(const message &msg){
    std::vector<tcp_connection::pointer>::iterator it = connections_.begin();
    for (;it != connections_.end(); ++it){
        (*it)->send(msg);
    }
}


void tcp_server::append_out_message(const message::pointer &msg){
    lock_guard lkgd(mutex_out_msg_);
    std::cout<<"Append out messages"<<std::endl;
    out_messages_.push_back(msg);
}

void tcp_server::append_in_message(const message::pointer &msg){
    lock_guard lkgd(mutex_in_msg_);
    std::cout<<"append in messages"<<std::endl;
    in_messages_.push_back(msg);
    std::cout<<"end append"<<std::endl;
}
message::pointer tcp_server::pick_in_message(){

    while(in_messages_.empty())
    {
         boost::this_thread::sleep(boost::posix_time::seconds(1));
    }
    std::cout<<"pick in mesage"<<std::endl;
    lock_guard lkgd(mutex_in_msg_);
    message::pointer msg = in_messages_.front();
    in_messages_.pop_front();
    return msg;
}

message::pointer tcp_server::pick_out_message(){
    while(out_messages_.empty()){
        boost::this_thread::sleep(boost::posix_time::seconds(1));
    }
    lock_guard lkgd(mutex_out_msg_);

    message::pointer msg = out_messages_.front();
    out_messages_.pop_front();
    return msg;
}
