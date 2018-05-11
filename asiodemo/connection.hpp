#include <boost/shared_ptr.hpp>
#include <boost/asio.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/bind.hpp>
#include <iostream>
#include <string>
#include <algorithm>

typedef boost::system::error_code error_code;
using boost::asio::ip::tcp;
using namespace boost;


class connection: public boost::enable_shared_from_this<connection>
//, boost::noncopyable
{

public:
    typedef boost::shared_ptr<connection> ptr;


public:
    connection(boost::asio::io_service &service)
        :sock_(service), started_(false)
    {

    }

    void start(){
        started_ = true;
        //clients.push_back(shared_from_this());
        do_read();
    }

    static ptr new_(boost::asio::io_service &ioservice){
      return ptr(new connection(ioservice));
  }

    tcp::socket& socket(){
        return sock_;
    }
    void stop(){
        if (!started()) return;

    }
    bool started(){
        return started_;
    }

    void do_read(){
        // boost::asio::async_read(sock_,
        //                         boost::asio::buffer(read_buffer_),
        //                         boost::bind(&connection::on_read,this,_1,_2));
        //boost::bind(&connection::on_read,this, _1, _2));

        //post_check_ping();
    }

    void do_write(const std::string &msg){
        if (!started()) return;

        std::copy(msg.begin(), msg.end(), write_buffer_);
        sock_.async_write_some(boost::asio::buffer(write_buffer_,msg.size()),
                               boost::bind(&connection::on_write,this, _1, _2));

    }

    void on_write(const boost::system::error_code &ec, size_t bytes){
        do_read();
    }

    void on_read(const boost::system::error_code &ec, size_t bytes){
        if (ec) stop();
        if (!started()) return;
        std::string msg(read_buffer_, bytes);
        if(msg.find("login ")==0) on_login(msg);
        //   else if (msg.find("ping")==0) on_ping();
        else if (msg.find("ask_clients") == 0) on_clients();
    }
    void on_clients(){
        std::cout<<"onclient"<<std::endl;
    }
    void on_login(const std::string &msg){
        std::cout<<"on login"<<msg<<std::endl;
    }

    void read_complete(boost::system::error_code &ec, size_t bytes){
        std::cout<< "read complete read bytes"<< bytes<<std::endl;
    }
    tcp::socket & sock(){return sock_;}
private:
    enum {max_msg = 1024};

    tcp::socket sock_;
    bool started_;
    char read_buffer_[max_msg];
    char write_buffer_[max_msg];
};
