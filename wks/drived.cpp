
#include <iostream>
#include <limits>
#include <functional>
using namespace std;
class Shape{
public:
  virtual void draw(){cout<<"I am a shape"<<endl;}
  void fun(){
    cout<<typeid(this).name()<<endl;
    draw();
  }
};

class Circle: public Shape{
public:
  void draw(){cout<<"I am a circle"<<endl;}
};
int global_int_var = 84;
int global_unit_var;
void func(int i){
  cout<<i<<endl;
}

struct OperateStar{
  Shape sp;
  Shape& operator*(){
    return sp;
  }
  Shape* operator->(){
    return &((*this).sp);
  }
};

void myprintf(const char*format,...){
  auto args = 0;
  const char* tmp = format;
  while(*tmp != '\0'){
    if(*tmp == '%'){
      args++;
    }
    tmp++;
  }
  cout<<args<<endl;
  const int* argsptr = (const int*)(&format);
  argsptr++;
  for(auto i = 0; i< args; i++){
    //cout<<(char*)*argsptr<<endl;
    argsptr++;
  }
}
void func_with_3_params(int a,int b, int c){
  cout<<a<<b<<c<<endl;
}
void func_interface(std::function<void(int ,int)> fn){
  fn(1,2);
}
void bind_princple(){
  auto bindfn3 = std::bind(func_with_3_params,1,std::placeholders::_1,std::placeholders::_2 );

  func_interface(bindfn3);
}
int main(){
  bind_princple();
  cout<<std::numeric_limits<unsigned char>::digits<<endl;
  cout<<std::numeric_limits<char>::digits<<endl;
  static int static_var =8;
  static int static_var2;
  int a = 1;
  int b=0;
  auto lmf = []()->decltype(b) {return 1;};
  lmf();
  func(static_var+static_var2+a+b);
  return 0;
}
