#include <cstddef>
#include <ctime>
#include <string>
#include <iostream>
#include <iterator>
#include <algorithm>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>
//#include "connection.hpp"

using boost::asio::ip::tcp;

std::string make_daytime_string(){
    using namespace std;
    time_t now = time(0);
    return ctime(&now);
}

class tcp_connection: public boost::enable_shared_from_this<tcp_connection>{
public:
    typedef boost::shared_ptr<tcp_connection> pointer;

    static pointer create(boost::asio::io_service &io_service){
        return pointer(new tcp_connection(io_service));
    }
    tcp::socket &socket(){
        return socket_;
    }

    void start(){
        message_ = make_daytime_string();

        boost::asio::async_write(socket_, boost::asio::buffer(message_),
                                 boost::bind(&tcp_connection::handle_write,
                                             shared_from_this(),
                                             boost::asio::placeholders::error,
                                             boost::asio::placeholders::bytes_transferred));

        boost::asio::async_read(socket_, boost::asio::buffer(data_, 3),
                                boost::bind(&tcp_connection::handle_read, shared_from_this(),
                                                 boost::asio::placeholders::error,
                                                 boost::asio::placeholders::bytes_transferred));
    }

private:
    tcp_connection(boost::asio::io_service &io_service)
        :socket_(io_service){

    }
    void handle_read(const boost::system::error_code &error,
                     size_t bytes_transferred){
        std::cout<<"handle read"<<std::endl;
        if (!error){
            boost::asio::async_write(socket_,
                                     boost::asio::buffer(data_, bytes_transferred),
                                     boost::bind(&tcp_connection::handle_write, shared_from_this(),
                                                 boost::asio::placeholders::error,
                                                 boost::asio::placeholders::bytes_transferred));

        }
        else{
            std::cout<<"ERROR"<<error<<" transferred"<<bytes_transferred<< std::endl;
        }
    }

    void handle_write(const boost::system::error_code &ec, size_t bytes_transferred){
        std::cout<<"aync write "<<message_<<std::endl;

        std::cout<<"bytes transferred "<<bytes_transferred<<std::endl;


    }

private:
    enum {max_length = 1024};
    char data_[max_length];
    tcp::socket socket_;
    std::string message_;
};

class tcp_server{

public:
    tcp_server(boost::asio::io_service &io_service)
        :acceptor_(io_service, tcp::endpoint(tcp::v4(), 8001)){

        start_accept();
    }

    void start_accept(){
        std::cout<<"start accept"<<std::endl;
        tcp_connection::pointer new_connection =
            tcp_connection::create(acceptor_.get_io_service());

        acceptor_.async_accept(new_connection->socket(),
                               boost::bind(&tcp_server::handle_accept, this, new_connection,
                                           boost::asio::placeholders::error));
    }

    void handle_accept(tcp_connection::pointer new_connection,
                       const boost::system::error_code &ec){

        std::cout<<"new connection"<<std::endl;
        if (!ec){
            new_connection->start();
        }
        start_accept();
    }
private:
    boost::asio::ip::tcp::acceptor acceptor_;

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
