#include <iostream>
#include <iterator>
#include <algorithm>
#include <vector>
#include <sstream>
using namespace std;
int main(){
  vector<int> v1={923,434,56,7,889,434,6547,1,4};
  vector<int> v2={2,434,67,885,344,34,1,4,24,6,7};
  vector<int> v3;
  sort(begin(v1), end(v1));
  sort(begin(v2), end(v2));
  set_intersection(begin(v1), end(v1), begin(v2), end(v2), back_inserter(v3));

  for(auto i: v3){
    cout<<i<<endl;
  }

  vector<int> v4;
  copy_if(begin(v1), end(v1),back_inserter(v4),[](int v){return v<100&&v>10;});
  for(auto i :v4){
    cout<<i<<endl;
  }
  stringstream strm;
  copy(begin(v1),  end(v1), ostream_iterator<int>(strm," "));
  cout<<strm.str()<<endl;
  return 0;
}
