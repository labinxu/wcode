#include <deque>
#include <iostream>
#include <boost/array.hpp>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/thread.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <algorithm>
#include <iterator>
#include <string>
#include "../message.hpp"
using boost::asio::ip::tcp;
using namespace boost::asio;

//https://www.boost.org/doc/libs/1_39_0/doc/html/boost_asio/example/chat/chat_client.cpp
typedef std::deque<message> message_queue;

class tcp_client :public boost::enable_shared_from_this<tcp_client>{
public:
    tcp_client(boost::asio::io_service &io_service,
               tcp::endpoint &endpoint)
        :io_service_(io_service),socket_(io_service){

        socket_.async_connect(endpoint,
                              boost::bind(&tcp_client::handle_connect,
                                          this,
                                          placeholders::error));

    }

    void close(){
        std::cout<<"client close"<<std::endl;
    }
    // void send(const message &msg){
    //     std::cout<<"send "<<msg.body()<<std::endl;
    //     io_service_.post(boost::bind(&tcp_client::do_send,
    //                                  this, msg));
    // }


private:
    boost::asio::ip::tcp::endpoint endpoint_;
    boost::asio::io_service &io_service_;
    tcp::socket socket_;;

public:
    void send(message msg){
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
private:
    void handle_write(const boost::system::error_code &ec){
        if(ec){
            std::cout<<"ERROR "<<boost::system::system_error(ec).what()<<std::endl;
        }

    }

    void handle_read(const boost::system::error_code &ec, size_t bytes_transferred){

        std::cout<<"handle read"<<std::endl;

    }
    void handle_read_header(const boost::system::error_code &error,
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
        }

    }

    void handle_read_body(const boost::system::error_code &error){
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

    void handle_connect(const boost::system::error_code &error){
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
            std::cout<<"connection losted"<<std::endl;
        }
    }
private:
    message received_msg_;
    message_queue send_msgs_;
};

int main(){

    try{
        boost::asio::io_service io_service;
        tcp::endpoint endpoint(boost::asio::ip::address::from_string("127.0.0.1"), 8001);
        tcp_client client(io_service, endpoint);
        boost::thread t(boost::bind(&boost::asio::io_service::run,
                                    &io_service));

        while(true)
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
