#include <string>
#include <vector>
#include "argument.hpp"

namespace Args{
    using namespace std;

    class Parser{
    public:
        Parser(const string &name):name_(name){}
    private:
        string name_;
    };

    class SubParser{
    public:
        SubParser(const string &title,
                  const string &dest,
                  const string &description="",
                  const string &help=""){
        }

    private:
        string tile_;
        string dest_;
        string description_;
        string help_;
    };

    class Argparse{
    public:
        Argparse(const string &prog):prog_(prog){
        }
        Argparse():prog_(""){}
        void add_argument(const string &shortarg="",
                          const string &longarg="",
                          const string &defval="",
                          const string help="",
                          const bool required=false,
                          const ParamType argtype=Str){

            Argument* arg = new Argument(shortarg,
                                         longarg,
                                         defval,
                                         help,
                                         required,
                                         argtype);
            arguments_.push_back(arg);
        }

        void ParseArgs(){
            //
        }
    private:
        vector<Argument*> arguments_;
        string prog_;
    };

}

int main(){
    Args::Argparse argparser("demo");
    argparser.add_argument("-t","--test",argtype=Int);

}


