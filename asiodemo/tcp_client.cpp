#include <deque>
#include <iostream>
#include <boost/array.hpp>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/thread.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <algorithm>
#include <iterator>
#include <map>
#include <string>
#include "message.hpp"
#include "tcp_client.h"


tcp_client::tcp_client(boost::asio::io_service &io_service,
                       tcp::endpoint &endpoint)
    :io_service_(io_service),
     endpoint_(endpoint),
     socket_(io_service),
     active_(true){

    socket_.async_connect(endpoint,
                          boost::bind(&tcp_client::handle_connect,
                                      this,
                                      placeholders::error));
}
void tcp_client::reconnect(){
    std::cout<<"re connect"<<std::endl;
    socket_.async_connect(endpoint_,
                          boost::bind(&tcp_client::handle_connect,
                                      this,
                                      placeholders::error));
}

void tcp_client::close(){
    std::cout<<"client close"<<std::endl;
}


bool tcp_client::isActive(){
    return active_;
}

void tcp_client::send(const message &msg){
    io_service_.post(boost::bind(&tcp_client::do_send, this, msg));
}

void tcp_client::do_send(const message &msg){
    boost::asio::async_write(socket_,
                             boost::asio::buffer(msg.data(), msg.length()),
                             boost::bind(&tcp_client::handle_write,
                                         this,
                                         placeholders::error));

    // boost::asio::async_read(socket_,
    //                         boost::asio::buffer(received_msg_.data(),
    //                                             message::header_length),
    //                         boost::bind(&tcp_client::handle_read_header,
    //                                     this,
    //                                     placeholders::error,
    //                                     placeholders::bytes_transferred));
}

void tcp_client::handle_write(const boost::system::error_code &ec){
    if(ec){
        std::cout<<"ERROR "<<boost::system::system_error(ec).what()<<std::endl;
    }

}

void tcp_client::handle_read(const boost::system::error_code &ec, size_t bytes_transferred){

    std::cout<<"handle read"<<std::endl;

}
void tcp_client::handle_read_header(const boost::system::error_code &error,
                                    size_t bytes_transferred){

    if (!error && received_msg_.decode_header()){
        boost::asio::async_read(socket_,

                                boost::asio::buffer(received_msg_.body(),
                                                    received_msg_.body_length()),

                                boost::bind(&tcp_client::handle_read_body,
                                            this,
                                            placeholders::error)
            );

    }
    else{
        std::cout<<"disconnected!"<<std::endl;
        active_ = false;
    }

}

void tcp_client::handle_read_body(const boost::system::error_code &error){
    if (!error){
        std::cout<<"From Server:";
        std::cout.write(received_msg_.body(), received_msg_.body_length());
        std::cout<<std::endl;

        boost::asio::async_read(socket_,
                                boost::asio::buffer(received_msg_.data(),
                                                    message::header_length),
                                boost::bind(&tcp_client::handle_read_header,
                                            this,
                                            placeholders::error,
                                            placeholders::bytes_transferred));
    }
    else{
        std::cout<<"handle read body error"<<std::endl;
    }
}

void tcp_client::handle_connect(const boost::system::error_code &error){
    if (!error){
        boost::asio::async_read(socket_,
                                boost::asio::buffer(received_msg_.data(),
                                                    message::header_length),

                                boost::bind(&tcp_client::handle_read_header,
                                            this,
                                            placeholders::error,
                                            placeholders::bytes_transferred));

        // message msg("Hello Server");
        // msg.encode_header();
        // boost::asio::async_write(socket_,
        //                          boost::asio::buffer(msg.data(), msg.length()),
        //                          boost::bind(&tcp_client::handle_write,
        //                                      this,
        //                                      placeholders::error));

        std::cout<<"connected"<<std::endl;

    }
    else {
        // try to reconnect
        std::cout<<"connection losted"<<boost::system::system_error(error).what()<<std::endl;
        //boost::system::system_error ero(error);
        reconnect();
    }
}
boost::asio::io_service& tcp_client::get_service(){
    return io_service_;
}

// static tcp_client::pointer tcp_client::create(boost::asio::io_service &io_service,
//                                               const std::string &address, int port){

//     tcp::endpoint endpoint(ip::address::from_string(address.c_str()), port);
//     tcp_client::pointer client(new tcp_client(io_service, endpoint));
// }
