#include <algorithm>
#include <vector>
#include <iterator>
#include <iostream>
using namespace std;
struct MyFunctor{
  MyFunctor():sum(0){}
  int sum;
  int operator()(int a){
    return sum+=a;
  }
};

int main(){
  std::vector<int> vints={1,2,3,4,5,6,7,8,9,10};
  auto rest = for_each(std::begin(vints),std::end(vints),MyFunctor());
  cout<<"function object result: "<<rest.sum<<endl;

  int sum = 0 ;
  for_each(std::begin(vints),std::end(vints),[&sum](int &a){sum+=a;});
  cout<<"lambda function result: "<<sum<<endl;

  int a = 0;
  auto mutablefn = [=]() mutable{ a=2;};
  mutablefn();
  cout<<"mutablefn:"<<a<<endl;
  return 0;
}
