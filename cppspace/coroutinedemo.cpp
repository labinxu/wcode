#include <tuple>
#include <string>
#include <iostream>
#include <boost/coroutine2/all.hpp>
#include <boost/bind.hpp>
#include <boost/tuple/tuple.hpp>
#include <boost/lambda/lambda.hpp>
#include <string>
using namespace std;
using boost::coroutines2::coroutine;

void cooperative(coroutine<std::tuple<int, std::string>>::pull_type &source)
{
    std::string str;
    auto args = source.get();
    std::cout << std::get<0>(args) <<" "<<std::get<1>(args)<<std::endl;
    source();
    source();
    args = source.get();
    std::cout<<std::get<0>(args)<<" "<<std::get<1>(args)<<std::endl;

}

int main()
{
    std::string str1("aaa");
    std::string str2("bbb");
    coroutine<std::tuple<int, std::string>>::push_type sink{cooperative};
    sink(std::make_tuple(0, str1));
    sink(std::make_tuple(1, str2));
    std::cout<<std::endl;
    string str;
    
}
