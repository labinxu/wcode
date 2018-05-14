#include <string>
#include <vector>
namespace Args{
    using namespace std;

    typedef enum {Int=1,Str,Bool} ParamType;

    class Argument{
    public:
        Argument(const string &shortarg="",
                 const string &longarg="",
                 const string defval="",
                 const string help="",
                 bool required=false,
                 ParamType paramType=Str)
            :shortArg_(shortarg),
             longArg_(longarg),
             defVal_(defval),
             help_(help),
             required_(required),
             paramType_(paramType){
        }

    private:
        string shortArg_;
        string longArg_;
        string defVal_;
        string help_;
        bool required_;
        ParamType paramType_;
    };
}
