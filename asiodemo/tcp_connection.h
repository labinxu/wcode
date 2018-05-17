#ifndef TCP_CONNECTION_H
#define TCP_CONNECTION_H

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

using namespace boost::asio;
using boost::asio::ip::tcp;

class tcp_server;
class tcp_connection: public boost::enable_shared_from_this<tcp_connection>{
public:
    typedef boost::shared_ptr<tcp_connection> pointer;
    tcp::socket &socket();

    void start();

    tcp_connection(boost::asio::io_service &io_service,tcp_server *server);

    void set_client(const tcp_client::pointer client);
    void send(const message &msg);
    void do_send(const message &msg);

    void close();
private:
    void message_handle_loop();
    void handle_write(const boost::system::error_code &ec);
    void handle_read_header(const boost::system::error_code &error);

    void handle_read_body(const boost::system::error_code &error);
    void handle_read(const boost::system::error_code &error);

private:
    boost::asio::io_service &io_service_;
    tcp_client::pointer client_;
    tcp::socket socket_;
    message read_msg_;
    bool active_;
    tcp_server *server_;
};
#endif
