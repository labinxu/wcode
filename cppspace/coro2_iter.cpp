#include <iostream>
#include <boost/coroutine2/all.hpp>
#include <boost/coroutine2/detail/push_coroutine.hpp>
#include <boost/coroutine2/detail/pull_coroutine.hpp>

constexpr int N = 10;
typedef boost::coroutines2::coroutine<int>::pull_type coro2_pull_t;
typedef boost::coroutines2::coroutine<int>::push_type coro2_push_t;

void foo(coro2_pull_t &sink)
{
    for(auto val: sink)
    {
        std::cout<<"retrieve "<<val<<std::endl;
        sink();
    }
}
void boo(coro2_pull_t &sink)
{
    for(auto val:sink)
    {
        std::cout<<"retrieve "<<val<<std::endl;
        sink();
    }
}

int main()
{
    coro2_push_t source(foo);
    for (int i=0; i < N; ++i)
    {
        source(i);
    }
    coro2_push_t src(boo);

    for(auto c:"abcdefg")
    {
        if (c != '\0')
            src(c);
    }
}
