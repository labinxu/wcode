#include <cstddef>
#include <ctime>
#include <deque>
#include <string>
#include <iostream>
#include <iterator>
#include <algorithm>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>
//#include "connection.hpp"
#include "message.hpp"
typedef std::deque<message> message_queue;
using namespace boost::asio;
using boost::asio::ip::tcp;

std::string make_daytime_string(){
    using namespace std;
    time_t now = time(0);
    return ctime(&now);
}


class tcp_connection:public boost::enable_shared_from_this<tcp_connection>{
public:
    typedef boost::shared_ptr<tcp_connection> pointer;
    tcp::socket &socket(){
        return socket_;
    }

    void start(){
        // message_ = make_daytime_string();
        // message msg(message_);
        // msg.encode_header();

        // std::cout<<"starting connection"<<std::endl;
        // boost::asio::async_write(socket_,
        //                          boost::asio::buffer(msg.data(), msg.length()),
        //                          boost::bind(&tcp_connection::handle_write,
        //                                      this,
        //                                      placeholders::error,
        //                                      placeholders::bytes_transferred));

        // boost::asio::async_read(socket_,
        //                         boost::asio::buffer(read_msg_.data(),
        //                                             message::header_length),

        //                         boost::bind(&tcp_connection::handle_read_header,
        //                                     this,
        //                                     placeholders::error));

        boost::asio::async_read(socket_,
                                boost::asio::buffer(read_msg_.data(),
                                                    message::header_length),
                                boost::bind(&tcp_connection::handle_read_header,
                                            shared_from_this(),
                                            placeholders::error));
    }


    tcp_connection(boost::asio::io_service &io_service)
        :socket_(io_service){

    }

private:

    void handle_read_header(const boost::system::error_code &error){
        std::cout<<"handle read header"<<std::endl;
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
        }
        std::cout<<error<<"=="<<read_msg_.body_length()<<std::endl;

    }

    void handle_read_body(const boost::system::error_code &error){

        if (!error){
            //std::cout.write(read_msg_.body(), read_msg_.body_length());
            //std::cout<<std::endl;

            boost::asio::async_read(socket_,
                                     boost::asio::buffer(read_msg_.data(),
                                                         message::header_length),
                                     boost::bind(&tcp_connection::handle_read_header,
                                                 shared_from_this(),
                                                 placeholders::error));
        }
        else{
                std::cout<<"handle read_body error "<<error<<std::endl;

        }
    }

    void handle_read(const boost::system::error_code &error){
        std::cout<<"handle read "<<read_msg_.body()<< std::endl;
        if (!error){

            // boost::asio::async_write(socket_,
            //                          boost::asio::buffer(data_, bytes_transferred),
            //                          boost::bind(&tcp_connection::handle_write, shared_from_this(),
            //                                      boost::asio::placeholders::error,
            //                                      boost::asio::placeholders::bytes_transferred));

        }
        else{
            boost::system::system_error e=boost::system::system_error(error);

            std::cout<<"handle read error"<<e.what()<< std::endl;
        }
    }

    void handle_write(const boost::system::error_code &ec, size_t bytes_transferred){
        std::cout<<"bytes transferred "<<bytes_transferred<<std::endl;
    }

private:
    tcp::socket socket_;
    message read_msg_;
};

class tcp_server{

public:
    tcp_server(boost::asio::io_service &io_service)
        :io_service_(io_service),
        acceptor_(io_service,
                   tcp::endpoint(boost::asio::ip::address::from_string("127.0.0.1"), 8001)){

        tcp_connection::pointer new_connection(new tcp_connection(io_service_));

        acceptor_.async_accept(new_connection->socket(),
                               boost::bind(&tcp_server::handle_accept,
                                           this,
                                           new_connection,
                                           boost::asio::placeholders::error));
    }

    void handle_accept(tcp_connection::pointer new_connection,
                       const boost::system::error_code &ec){

        std::cout<<"new connection"<<std::endl;
        if (!ec){
            new_connection->start();
            tcp_connection::pointer new_connection(new tcp_connection (io_service_));
            acceptor_.async_accept(new_connection->socket(),
                                   boost::bind(&tcp_server::handle_accept,
                                               this,
                                               new_connection,
                                               boost::asio::placeholders::error));
        }
    }

private:
    boost::asio::ip::tcp::acceptor acceptor_;
    boost::asio::io_service &io_service_;

};


int main(){
    try{
        boost::asio::io_service io_service;
        tcp_server server(io_service);
        io_service.run();
    }
    catch(std::exception &e){
        std::cerr<<e.what()<<std::endl;
    }
    return 0;
    // connection::ptr client = connection::new_(service);
    // acceptor.async_accept(client->sock(), boost::bind(handle_accept, client, _1));
    // service.run();
}
