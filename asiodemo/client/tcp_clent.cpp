#include <deque>
#include <iostream>
#include <boost/array.hpp>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/thread.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <algorithm>
#include <iterator>
#include "../message.hpp"
using boost::asio::ip::tcp;
//https://www.boost.org/doc/libs/1_39_0/doc/html/boost_asio/example/chat/chat_client.cpp
typedef std::deque<message> message_queue;
class tcp_client{// :public boost::enable_shared_from_this<tcp_client>{
public:
    tcp_client(boost::asio::io_service &io_service,
               tcp::endpoint &endpoint)
        :io_service_(io_service),socket_(io_service){
        socket_.async_connect(endpoint,
                              boost::bind(&tcp_client::handle_connect,
                                          this,
                                          boost::asio::placeholders::error));

    }

    void close(){
        std::cout<<"client close"<<std::endl;
    }
    void send(const char*msg){
        std::cout<<"send "<<msg<<std::endl;
        std::copy(msg, msg+strlen(msg), buf.begin());
        io_service_.post(boost::bind(&tcp_client::do_send,
                                     this));
    }
private:
    boost::asio::ip::tcp::endpoint endpoint_;
    boost::asio::io_service &io_service_;
    tcp::socket socket_;;
    boost::array<char, 25> buf;

private:
    void do_send(){
        boost::asio::async_write(socket_,
                                 boost::asio::buffer(buf, 25),
                                 boost::bind(&tcp_client::handle_write,
                                             this,
                                             boost::asio::placeholders::error,
                                             boost::asio::placeholders::bytes_transferred));
    }

    void handle_write(const boost::system::error_code &ec, size_t bytes_transferred){
        if(!ec){
            std::cout<<"handle write msg"<<std::endl;
        }
    }

    void handle_read(const boost::system::error_code &ec, size_t bytes_transferred){
        std::cout<<buf.data()<<std::endl;
        std::cout<<"handle read"<<std::endl;

    }
    void handle_connect(const boost::system::error_code &error){
        boost::asio::async_read(socket_, boost::asio::buffer(buf),
                               boost::bind(&tcp_client::handle_read,
                                           this,
                                           boost::asio::placeholders::error,
                                           boost::asio::placeholders::bytes_transferred));
        std::cout<<"handle connect"<<std::endl;
    }
};
int main(){

    try{
        boost::asio::io_service io_service;
        tcp::endpoint endpoint(boost::asio::ip::address::from_string("127.0.0.1"), 8001);
        tcp_client client(io_service, endpoint);
        boost::thread t(boost::bind(&boost::asio::io_service::run,
                                    &io_service));

        char line[message::max_body_length+1];
        while(true)
        {
            std::cin.getline(line,3);
            if (line[0]='Q'){
                break;
            }
            std::cout<<"line"<<std::endl;
            client.send(line);

        }
        client.close();
        t.join();
        //t.join();
    }
    catch (std::exception &e){
        std::cerr<<e.what()<<std::endl;
    }
}
