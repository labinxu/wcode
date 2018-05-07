#ifndef NLS_SIM_CONNECTION_H_
#define NLS_SIM_CONNECTION_H_
#include <boost/asio.hpp>
#include <memory>
#include <string>

class Nls_sim_connection : public std::enable_shared_from_this<Nls_sim_connection>{
public:
  explicit Nls_sim_connection(boost::asio::ip::tcp &&socket);
  void start();
  void async_send(const void *data, size_t len);
  void async_send(const std::string &data);
  void callback(const )
}

#enddef
