#include <iostream>
#include <string>
using namespace std;
enum MsgType{one, two,three};
class Message{
public:
  Message(const MsgType &msgT, const string &data)
    :_msgType(msgT),_data(data){}
  const MsgType getMsgType() const {return _msgType;}
private:
  string _data;
  MsgType _msgType;
};
class MessageOne:public Message{};
class MessageTwo:public Message{};
class MessageThree:public Message{};

void handle_message(Message *msg){
  auto msgType = msg->getMsgType();
  switch(msgType){
  case one:

    cout<<"message type one"<<endl;
    break;
  case two:
    break;
  case three:
    break;
  default:
    break;
  }
}
template<typename T>
class HandleMessage{
  
};
template<MsgType>
class HandleMessage{
  HandleMessage(Message&msg){
    cout<<"handle message type is one"<<endl;
  }
};
int main(){
  Message msg(one, "one");
  handle_message(&msg);
  auto mt = msg.getMsgType();
  HandleMessage<one> hm(msg);
  return 0;
}
