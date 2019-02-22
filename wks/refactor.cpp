#include <functional>
#include <tuple>
#include <map>

using namespace std;
using namespace std::placeholders;
map<int, function<void(int,int,int)>> signalData;
void task(int a, int b, int c){
}
void initSigData(){
  signalData = {
                {1, std::bind(task, _1, _2, _3)},
  };
}
int main(){
  
}
