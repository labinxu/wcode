#include <iostream>
#include <algorithm>
#include <string.h>
using namespace std;
template <class T>
class Singleton
{
protected:
  Singleton(){}
public:
  static T* getInstance()
  {

    if(instance == NULL)
      {
        instance = new T();
      }
    return instance;
  }
  static T *instance;
};
template<class T>
T* Singleton<T>::instance = NULL;


class TestSingleton:public Singleton<TestSingleton>
{
  friend class Singleton;
private:
  TestSingleton(){}
public:
  void display(){
    std::cout<<"hello singleton"<<std::endl;
  }
};

int main()
{
  TestSingleton *t = TestSingleton::getInstance();
  t->display();
  //TestSingleton *t2 = new TestSingleton();
  //t2->display();
  //return 1;
  char pc[] = "abc.cdb.edf";

  // variable
  for(auto c: pc){
    if(c == '.'){
      c='/';
    }
  }

  // reference will change the value
  for(auto &c: pc)
  {
      if(c == '.')
      {
          c='/';
      }
  }
  std::cout<<pc<<std::endl;

  // reference change the value
  for_each(pc, pc+strlen(pc), [](char& c){
      if(c=='.'){
        c='/';
      }
    });
  std::cout<<pc<<std::endl;

}
