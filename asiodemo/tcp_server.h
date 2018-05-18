#include <cstddef>
#include <ctime>
#include <string>
#include <iostream>
#include <iterator>
#include <algorithm>
#include <vector>
#include <deque>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/tuple/tuple.hpp>
#include <boost/thread.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>

#include "tcp_client.h"
#include "tcp_connection.h"
#include "message.hpp"

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
};

