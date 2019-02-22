// #include <SFML/Graphics.hpp>
#include <iostream>
#include <limits>
#include <type_traits>
using namespace std;
int main(){
  cout<<std::numeric_limits<int>::min()<<endl;
  cout<<std::numeric_limits<int>::max()<<endl;
  cout<<std::numeric_limits<unsigned int>::min()<<endl;
  cout<<std::numeric_limits<unsigned int>::max()<<endl;
}
