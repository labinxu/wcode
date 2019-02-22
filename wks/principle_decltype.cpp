#include<iostream>
#include<typeinfo>
using namespace std;

class CTest
{
public:
    int m_iNum;
};

void overloadfunc(int)
{}
void overloadfunc(char)
{}
int && rxvale();
const bool func(){
    return true;
}

int main(){
  int itest = 3;
  int arr[3] = { 0 };
  int *pInt = arr;
  decltype(arr)   darr;      //int *
  cout << typeid(darr).name() << endl;
  decltype(pInt)   dpInt;      //int *
  cout << typeid(dpInt).name() << endl;
  CTest clTest;
  decltype(clTest.m_iNum)   dClTestNum;   //int 
  cout << typeid(dClTestNum).name() << endl;
  //decltype(overloadfunc);      //编译不通过

    //带括号 规则 1
    decltype(rxvale()) drxvalue = 1;    //将亡值 int &&
    cout << typeid(drxvalue).name() << endl;

    //带括号 规则2
    decltype(true ? itest : itest) ditest1 = itest;    //int& 三元运算符，这里返回一个itest的左值
    cout << typeid(ditest1).name() << endl;
    decltype((itest)) ditest2 = itest;    //int&  itest的左值
    cout << typeid(ditest2).name() << endl;

    decltype((++itest)) ditest3 = itest;    //int&  itest的左值
    cout << typeid(ditest2).name() << itest << ditest3 << endl;   // 3,3
    decltype(arr[1])   darr1 = itest;       //int& [] 操作返回左值
    cout << typeid(darr1).name() << darr1 << endl;

    decltype(*pInt)   dpInt1 = itest;       //int&  *操作返回左值
    cout << typeid(dpInt1).name() << dpInt1 <<  endl;

    decltype("hello") dstr = "world";      //const char(&)[6] 字符串字面常量为左值
    // 带括号 规则3 推导为本类型
    cout<<dstr<<endl;
    decltype(12) dNum = 100;               //int
    cout << typeid(dNum).name() << dNum << endl;
    decltype(itest++) dNum1 = 0;           //int  itest++返回右值
    cout << typeid(dNum1).name() << dNum1 << endl;
    decltype(func()) dFunc = true;         //const bool  推导为bool
    cout << typeid(dFunc).name() << dFunc << endl;
    return 0;
}
