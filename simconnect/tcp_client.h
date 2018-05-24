#ifndef TCP_CLIENT_H
#define TCP_CLIENT_H

#include <iostream>
#include <boost/array.hpp>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/thread.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/function.hpp>
#include <algorithm>
#include <iterator>
#include <map>
#include <string>
#include "message.hpp"
using boost::asio::ip::tcp;
using namespace boost::asio;

//https://www.boost.org/doc/libs/1_39_0/doc/html/boost_asio/example/chat/chat_client.cpp

class tcp_server;
typedef boost::function<void (message::pointer)> message_handler;
class tcp_client{//} :public boost::enable_shared_from_this<tcp_client>{
public:
    typedef boost::shared_ptr<tcp_client> pointer;

    tcp_client(boost::asio::io_service &io_service,
               tcp::endpoint &endpoint,
               tcp_server *local_server=NULL);

    void close();

    void connect();
public:
    bool active();
    void send(const message &msg);
    void do_send(const message &msg);
private:
    void reconnect();
    void handle_write(const boost::system::error_code &ec);
    void handle_read(const boost::system::error_code &ec, size_t bytes_transferred);


    void handle_read_header(const boost::system::error_code &error,
                            size_t bytes_transferred);

    void handle_read_body(const boost::system::error_code &error);


    void handle_connect(const boost::system::error_code &error);

public:
    boost::asio::io_service& get_service();
    void set_message_handler(message_handler &mh);
    //static tcp_client::pointer create(boost::asio::io_service &io_service,
    //const std::string &address, int port);
private:
    void simulate_send_message();

private:
    tcp_server *local_server_;
    boost::asio::io_service &io_service_;
    tcp::socket socket_;
    boost::asio::ip::tcp::endpoint endpoint_;
    message_handler message_handler_;
    message received_msg_;
    std::map<std::string, message> events_;
    bool active_;
};

#endif
