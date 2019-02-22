#include <iostream>
#include <memory>
#include <functional>
#include <array>
#include <initializer_list>
#include <vector>
#include <algorithm>
#include <map>
#include <sstream>
#include <string>
#
using namespace std;
using namespace std::placeholders;
template<class T>
struct SimpleSmartPointer{
	SimpleSmartPointer(T *t):tptr(t){}
	~SimpleSmartPointer(){
    cout<<"release the pointer:"<<*tptr<<endl;
		if(tptr) delete tptr;
	}
  T* tptr;
// private:
// 	void* operator new(size_t size);
// 	void operator delete (void *p);

};

// auto keyword
auto test_auto(int a){
  return a;
}

void test_nullptr(int *i){
  cout<<"call test_nullptr(int *i)"<<endl;
}
void test_nullptr(int i){
  cout<<"call test_nullptr(int i)"<<endl;
}

int main(){
  //1. smart pointer 
  //will call destructor before return
	SimpleSmartPointer<int> sp1(new int(0));

	//SimpleSmartPointer<int> *sp2 = new SimpleSmartPointer<int>(int(1));
  SimpleSmartPointer<int> sp2(new int(1));
  // double delete
  // sp2 = sp1;

  // call destructor before return
  std::shared_ptr<int> sp3(new int(2));
  std::shared_ptr<int> sp4(new int(3));
  cout<<sp3.use_count()<<endl;
  //
  sp3 = sp4;
  cout<<sp3.use_count()<<endl;


  std::unique_ptr<int> up1(new int(4));
  cout<<*up1<<endl;
  // error:released pointer
  // cout<<*up1.release()<<endl;
  // cout<<*up1<<endl;

  std::unique_ptr<int> up2;
  up2 = std::move(up1);
  cout<<*up2<<endl;
  // cout<<*up1<<endl;// error dangling pointer ownership moved


  // weak pointer
  std::shared_ptr<int> sp (new int(5));
  std::weak_ptr<int> wp1;
  std::weak_ptr<int> wp2 (wp1);
  std::weak_ptr<int> wp3 (sp);

  std::cout << "use_count:\n";
  std::cout << "wp1: " << wp1.use_count() << '\n';
  std::cout << "wp2: " << wp2.use_count() << '\n';
  std::cout << "wp3: " << wp3.use_count() << '\n';

  //
  std::shared_ptr<int> spwk(wp3);
  cout<<"spwk: "<<spwk.use_count()<<"\n";

  //2. auto
  // auto err_deduce;// error, auto only deduced from a value.
  auto a = test_auto(6);
  cout<<typeid(a).name()<<endl; // i
  auto fv = 0.1f;
  cout<<typeid(fv).name()<<endl; // f
  auto dv = 0.1;
  cout<<typeid(dv).name()<<endl; // d
  cout<<typeid(sp).name()<<endl;// St10shared_ptrIi
  std::function<void()> fn = [](){cout<<"lambda func 1"<<"\n";};
  fn(); // lambda func 1

  auto fn2 = [](){cout<<"lambda func 2"<<"\n";};
  fn2(); // lambda func 2

  // decltype anti-function for auto
  auto ai = 0;
  cout<<"ai type is: "<<typeid(ai).name()<<endl;
  decltype(ai) ai1;
  cout<<"decltype ai1: "<<typeid(ai1).name()<<endl;
  // nullptr keyword
    // test_nullptr(NULL);// error: call of overloaded 'test_nullptr(NULL)


  test_nullptr(nullptr);


  // the initialize list syntax
  std::array<int,4> intarray = {1,2,3,4};
  //or std::array<int,4> intarray{1,2,3,4};
  cout<<"foreach: ";
  // 在C++中for循环可以使用类似java的简化的for循环，可以用于遍历数组，
  //容器，string以及由begin和end函数定义的序列（即有Iterator），示例代码如下：
  for(auto i: intarray){
    cout<<i<<" ";
  }

  cout<<"end foreach"<<"\n";
  std::vector<int> vints = {5,6,7,8};
  // lambda bind
  std::for_each(std::begin(vints),std::end(vints),[](int &i){i*=i;});
  cout<<"for vector:";
  for(auto i: vints){
    cout<<i<<" ";
  }
  cout<<"\n";

  // void lambda
  // [capture list] (params list) mutable exception-> return type { function body }
  // [=, &x], [&, x]
  int capturevar=0;
  // can't change the capture variable while pass by value
  cout<<"lambda capture: "<<capturevar<<endl;
  auto lam_var_pass = [capturevar](){cout<<"lambda capture 1: "<<capturevar<<endl;};
  capturevar = 10;
  lam_var_pass(); // lambda capturevar: 0.;
  auto lam_var_pass1 = [&capturevar](){cout<<"lambda capture 2: "<<++capturevar<<endl;};// 101
  capturevar = 100;
  lam_var_pass1(); // lambda capturevar: 100.;
  cout<<"lambda capturevar: "<<capturevar<<endl;
  //auto retfn2 = [](int param) -> int { return param*2;};
  auto retfn2 = [](int param) -> decltype(capturevar) { return param*2;};
  cout<<"lambda retfn2: "<<retfn2(2)<<endl; // lambda retfn2: 4

  // before c++11 bind1st bind2st ...
  // _1 _2 ... placeholders //using namespace placeholders
  // bind function
  auto bindfn1 = std::bind([](auto a, int b){return a+b;},2,_1);
  cout<<"bind fn1: "<<bindfn1(2)<<endl; // bind fn1: 4
  auto bindfn2 = std::bind([](int a, int b){return a+b;},_2,_1);
  cout<<"bind fn2: "<<bindfn2(4,4)<<endl; // bind fn1: 8

  // bind member function
  struct ClassForBind{
    void display(int a){cout<<"ClassForBind: "<<a<<endl;};
  };
  ClassForBind cfb;
  auto bindmemfn1 = bind(&ClassForBind::display,cfb,_1);
  bindmemfn1(1);// ClassForBind 1
  auto bindmemfn2 = bind(&ClassForBind::display,cfb,2);
  bindmemfn2();// ClassForBind 2
  // member function namemanaging


  // output a map to string
  map<string, string> strmap;
  strmap["key1"]="1";
  strmap["key2"]="2";
  stringstream strm;
  // version1
  for_each(strmap.begin(),strmap.end(),
           [&](const map<string,string>::value_type &v){
             strm<<"key:"<<v.first<<" = value: "<<v.second<<"\n";});
  cout<<strm.str()<<endl;

	return 0;
}
