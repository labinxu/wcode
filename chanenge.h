#pragma once


　


#include <stdint.h>


#include <string>


// company's order identifier
struct OrderIdentifier{
  OrderIdentifier() = default;
  OrderIdentifier(uint16_t m, uint16_t d, uint16_t t, uint32_t s)
    :_market(m)
    ,_desk(d)
    ,_trader(t)
    ,_sequence(s){
  }


  uint16_t _market{0};


  uint16_t _desk{0};


  uint16_t _trader{0};


  uint16_t _sequence{0}; // increments with each order from a particular trader
};


　


class IOrderManager{
  virtual bool OnTraderEnter(const OrderIdentifier &aInternal, uint32_t aPrice, uint32_t aQuantity) = 0;
  virtual bool OnTraderCancel(const OrderIdentifier & aInternal) = 0;


  virtual bool OnExchangeNew(const OrderIdentifier &aInternal, const std::string &aExternal) = 0 ;


  virtual bool OnExchangeTrade(const std::string &aExternal, uint32_t aQuantity) = 0;


  virtual bool OnExchangeCancle(const std::string &aExternal) const = 0;


  virtual bool IsOrderActive(const OrderIdentifier &aInternal) const = 0;


  virtual bool IsOrderActive(const std::string &aExternal) const = 0;


  // return the quantity of the order that is active in the market , or zero if hte order isn't recognised or is not active


  virtual uint32_t GetActiveOrderQuantity(const OrderIdentifier& aInternal) const = 0;


};
