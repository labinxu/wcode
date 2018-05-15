#include <cstddef>
#include <ctime>
#include <deque>
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
#include "tcp_connetion.hpp"
#include "message.hpp"
typedef std::deque<message> message_queue;

using namespace boost::asio;
using boost::asio::ip::tcp;


class tcp_server{

public:
    tcp_server(boost::asio::io_service &io_service,
               const std::string& address,
               int port)
        :io_service_(io_service),
        acceptor_(io_service,
                  tcp::endpoint(ip::address::from_string(address.c_str()), port)){

        tcp_connection::pointer new_connection(new tcp_connection(io_service_));
        acceptor_.async_accept(new_connection->socket(),
                               boost::bind(&tcp_server::handle_accept,
                                           this,
                                           new_connection,
                                           placeholders::error));
    }

    void handle_accept(tcp_connection::pointer new_connection,
                       const boost::system::error_code &ec){

        std::cout<<"new connection"<<std::endl;
        if (!ec){
            new_connection->start();
            connections_.push_back(new_connection);

            tcp_connection::pointer new_connection(new tcp_connection (io_service_));
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

private:
    std::vector<tcp_connection::pointer> connections_;
    boost::asio::io_service &io_service_;
    boost::asio::ip::tcp::acceptor acceptor_;

};

