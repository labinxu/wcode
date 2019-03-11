#include <iostream>
#include <vector>
using namespace std;
struct TestC{
  TestC(){cout<<"constructor TestC"<<endl;}
  ~TestC(){cout<<"distructor TestC"<<endl;}
};

int main(){
  vector<int*> vint1;
  int *p = new int (1);
  vint1.push_back(p);
  vector<int*> vint2;

  p = new int(2);
  vint2.push_back(p);

  for(auto i:vint1){
    cout<<*p<<endl;
  }

  for(auto i:vint2){
    cout<<*p<<endl;
  }

  return 0;
}
