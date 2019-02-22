#include <iostream>
using namespace std;
class Base{
public:
  virtual void foo(){cout<<"foo"<<endl;}
};
class Drived: public Base{
public:
  virtual void foo(){cout<<"Drived"<<endl;}
};
int foo(){
	int a = 1;
	int b = 2;
	cout<<a<<" "<<b<<endl;
	return 0;
}
int main1(){
	int c;
		int a;
	int b;
	cout<<"a="<<a<<"b="<<b<<c<<endl;
	return 0;

}
int main(){
foo();
main1();
	return 0;
}
