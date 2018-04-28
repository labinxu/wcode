#include <iostream>
#include <memory>
#include <array>
#include <boost/asio.hpp>
#include <string>
using boost::asio::ip::tcp;
using namespace std;


class Session :public std::enable_shared_from_this<Session>
{
public:
    Session(tcp::socket s)
        :socket_(std::move(s))
        {}

    void start(){
        async_read();
    }

private:
    void async_read()
    {
        //auto self = enable_shared_from_this();
        socket_.async_read_some(boost::asio::buffer(data_),
                                [this](const boost::system::error_code &ec, size_t bytes_transferred){
                                    if (!ec)
                                    {
                                          async_write(bytes_transferred);
                                    }
                                });

    }

     void async_write(std::size_t length){
         //auto self = enable_shared_from_this();
         boost::asio::async_write(socket_, boost::asio::buffer(data_,length),
                                  [this](const boost::system::error_code &ec, size_t bytes_transferred){
                                      if (!ec){
                                          async_read();
                                      }
                                  });
     }

    tcp::socket socket_;
    std::array<char, 1024> data_;
};

class Server
{
public:
    Server(boost::asio::io_service &io_service, short port)
        :acceptor_(io_service, tcp::endpoint(tcp::v4(), port)),
         socket_(io_service){

        async_accept();
    }
private:
    void async_accept(){
        acceptor_.async_accept(socket_,
                               std::bind(&Server::handle_accept,
                                         this, std::placeholders::_1));
    }

    void handle_accept(const boost::system::error_code &ec){
        if (!ec){
            std::shared_ptr<Session> sessionptr(new Session(std::move(socket_)));
            sessionptr->start();
        }
        async_accept();
    }

    tcp::acceptor acceptor_;
    tcp::socket socket_;
};

int main(){
    boost::asio::io_service io_service;
    Server s(io_service, 52014);
    io_service.run();
}
