#include <iostream>
#include <map>
#include <memory>
#include <algorithm>
#include <fstream>

typdefine map<string, map<string, string>> CfgData;
CfgData readCfgfile(const string &filename){
shared_ptr<fstream> fstrmptr(new fstream(filename),[](fstream *fs){fs->close();});
  auto trim = [](string &txt) -> string& {
    if(!txt.empty()){
        txt.erase(0,txt.find_first_not_of(" \n\r\t");
        txt.erase(txt.find_last_not_of(" \n\r\t")+1);
    }
    return txt;
  }
  
  string line,segname;
  CfgData cfgdata;
  while(getline(*(fstmptr.get()),line)){
    line=trim(move(line));
    if(line[0]=='#'){continue;}
    if(line[0]=='['){
    segname=trim(line.substr(1,line.size()-2);
    continue;
    }
    if(segname.empty()){continue;}
    auto pos = line.find('=');
    auto cfgitem = make_pair(trim(line.substr(0,pos),trim(line.substr(pos+1)));
    cfgdata[segname].insert(cfgitem);
  }
  return cfgdata;
}
int main(){
auto result = readIniFile("cfg.ini");
cout<<result["test"]["testitem"]
}
