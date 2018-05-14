#include <string>
#include <vector>
#include <iostream>
#include <map>
#include "argument.hpp"

namespace Args{
    using namespace std;

    class Parser{
    public:
        Parser(const string &name):name_(name){}

        string operator->(const string&name){
            auto end = namespace_.end();
            if(end != namespace_.find(name)){
                return namespace_[name];
            }

        }
    private:
        string name_;
        map<string,string> namespace_;
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

        void parse(){
            //
        }
    private:
        vector<Argument*> arguments_;
        string prog_;
    };

}

int main(){
    Args::Argparse argparser("demo");
    argparser.add_argument("-t","--test",argtype=Int, dest="adb");
    parser = argparser.parse();
    std::cout<<parser.adb<<std::endl;

}


