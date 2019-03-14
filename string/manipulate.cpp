#include <string>
#include <vector>
#include <iostream>
using namespace std;
std::vector<std::string>split(const string &text, char sep){
  string tmp;
  vector<string> ret;
  for(auto c:text){
    if(c != sep){
      tmp += c;
      continue;
    }
    // if (tmp.empty()){
    //   continue;
    // }
    ret.push_back(tmp);
    tmp.clear();
  }
  if(!tmp.empty()){
    ret.push_back(tmp);
  }
  return ret;
}
int main(){
  string text = ";ab;cd;ef;";
   auto ret = split( text, ';');
   for(auto v: ret){
     cout<<v<<endl;
   }
}
