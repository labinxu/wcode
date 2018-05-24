
#ifndef TCP_SERVER_H
#define TCP_SERVER_H

#include <string>
#include <algorithm>
#include <vector>
#include <deque>
#include <boost/tuple/tuple.hpp>
#include "tcp_client.h"
#include "tcp_connection.h"
#include "message.hpp"
#include "simconnect.h"

typedef std::deque<message::pointer> message_queue;

using namespace boost::asio;
using boost::asio::ip::tcp;


class tcp_server{
public:
    typedef boost::tuple<std::string, int> address;
    typedef boost::lock_guard<boost::mutex> lock_guard;

public:
    tcp_server(boost::asio::io_service &io_service,
               const address &hostaddress,
               const address &peer_server=boost::make_tuple("", 0));

    void handle_accept(tcp_connection::pointer new_connection,
                       const boost::system::error_code &ec);
    void send(const message &msg);
    void append_out_message(const message::pointer &msg);
    void append_in_message(const message::pointer &msg);
    void inmessage_handler(MsgHandler handler);
    void outmessage_handler(MsgHandler handler);
 protected:
    virtual void handle_out_message(const message::pointer &msg){};
    virtual void handle_in_message(const message::pointer &msg){};

 private:
    void handle_out_message();
    void handle_in_message();
    message::pointer pick_in_message();
    message::pointer pick_out_message();

private:
    std::vector<tcp_connection::pointer> connections_;
    boost::asio::io_service &io_service_;
    boost::asio::ip::tcp::acceptor acceptor_;
    address peer_server_;
    message_queue in_messages_;
    message_queue out_messages_;
    boost::mutex mutex_in_msg_;
    boost::mutex mutex_out_msg_;
    tcp_client::pointer client_;
    MsgHandler outmessage_handler_;
    MsgHandler inmessage_handler_;
};
#endif // 

