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
#include "tcp_client.h"
#include "tcp_server.h"
#include "tcp_connection.h"

using namespace boost::asio;
using boost::asio::ip::tcp;


tcp::socket& tcp_connection::socket(){
    return socket_;
}


void tcp_connection::start(){
    boost::asio::async_read(socket_,
                            boost::asio::buffer(read_msg_.data(),
                                                message::header_length),
                            boost::bind(&tcp_connection::handle_read_header,
                                        shared_from_this(),
                                        placeholders::error));
}

tcp_connection::tcp_connection(boost::asio::io_service &io_service,tcp_server *server)
    :io_service_(io_service),
     socket_(io_service),
     active_(true),
     server_(server){

     }

void tcp_connection::set_client(const tcp_client::pointer client){
    client_ = client;
}

void tcp_connection::send(const message &msg){
    io_service_.post(boost::bind(&tcp_connection::do_send,
                                 shared_from_this(),
                                 msg));

}

void tcp_connection::do_send(const message &msg){

    boost::asio::async_write(socket_,
                             boost::asio::buffer(msg.data(), msg.length()),
                             boost::bind(&tcp_connection::handle_write,
                                         shared_from_this(),
                                         placeholders::error));

}

void tcp_connection::close(){
    active_ = false;
    socket_.close();
}


void tcp_connection::message_handle_loop(){
    while(active_){

    }

}

void tcp_connection::handle_write(const boost::system::error_code &ec){
    if (ec){

        std::cout<<"handle write error"<<boost::system::system_error(ec).what()<<std::endl;

    }
}

void tcp_connection::handle_read_header(const boost::system::error_code &error){

    bool ret = read_msg_.decode_header();
    if (!error && ret){
        boost::asio::async_read(socket_,
                                boost::asio::buffer(read_msg_.body(),
                                                    read_msg_.body_length()),

                                boost::bind(&tcp_connection::handle_read_body,
                                            shared_from_this(),
                                            placeholders::error));

    }
    else{
        std::cout<<"disconnected!"<<std::endl;

        close();
    }


}

void tcp_connection::handle_read_body(const boost::system::error_code &error){

    if (!error){
        // std::cout<<"From Client:";
        // std::cout.write(read_msg_.body(), read_msg_.body_length());
        // std::cout<<std::endl;
        server_->append_in_message(read_msg_.clone());
        read_msg_.clear();

        boost::asio::async_read(socket_,
                                boost::asio::buffer(read_msg_.data(),
                                                    message::header_length),
                                boost::bind(&tcp_connection::handle_read_header,
                                            shared_from_this(),
                                            placeholders::error));
        // message msg("received");
        // msg.encode_header();
        // boost::asio::async_write(socket_,
        //                          boost::asio::buffer(msg.data(), msg.length()),
        //                          boost::bind(&tcp_connection::handle_write,
        //                                      shared_from_this(),
        //                                      placeholders::error));
    }
    else{
        std::cout<<"handle read_body error "<<error<<std::endl;

    }
}

void tcp_connection::handle_read(const boost::system::error_code &error){
    std::cout<<"handle read "<<read_msg_.body()<< std::endl;
    if (error){
        boost::system::system_error e=boost::system::system_error(error);

        std::cout<<"handle read error"<<e.what()<< std::endl;
    }
}
