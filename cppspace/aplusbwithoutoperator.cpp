#include <iostream>
using namespace std;

int bit_calc(int r, int c){
  if(c != 0){
    c<<=1;
    return bit_calc(r^c, r&c);
  }
  return r;
}
int aplusb(int a, int b)
{
  int r = a^b, c=a&b;
  return bit_calc(r, c);
}

int main()
{
  int  a = 3;
  int b = 12;
  cout<<aplusb(a, b);
  return 0;
}
