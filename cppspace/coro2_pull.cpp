#include <boost/coroutine2/all.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <iomanip>
using namespace std;

typedef boost::coroutines2::coroutine<int> coro_t;

void pulltype_demo()
{
    coro_t::pull_type source(
        [&](coro_t::push_type&sink)
        {
            int first = 1, second = 1;
            sink(first);
            sink(second);
            for (int i=0; i < 8; ++i)
            {
                int third = first + second;
                first = second;
                second = third;
                sink(third);
            }
        });


    for(auto i :source)
    {
        std::cout<<i<<endl;
    }

}
struct FinalEOL
{
    ~FinalEOL(){
        std::cout<<std::endl;
    }
};

void pushtypedemo()
{
    typedef boost::coroutines2::coroutine<std::string> coro_string_t;
    const int num = 5;
    const int width =  15;
    coro_string_t::push_type writer(
        [&](coro_string_t::pull_type &in)
        {
            FinalEOL finaleol;
            for(;;){
                for(int i=0; i<num;i++)
                {
                    if (!in) return;
                    std::cout<<std::setw(width)<<in.get();
                    in();
                }
            }
            std::cout<<std::endl;
        });
    std::vector<std::string> words{"pears", "porride", "Hot", "pess",
            "cold", "nine", "old","new"};

    std::copy(begin(words), end(words),begin(writer));
}

int main()
{
    pushtypedemo();
    pulltype_demo();
}
