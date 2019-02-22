#include <iostream>
#include <vector>
#include <utility>
#include <fstream>
#include <utility>
#include <fstream>
#include <iterator>
#include <string>
#include <boost/interprocess/file_mapping.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>
#include <iostream>
#include <fstream>
#include <boost/serialization/map.hpp>

using namespace boost::archive;
using namespace boost::interprocess;
void save()
{
  {
    std::ofstream file{"archive1.bin"};
    text_oarchive oa{file};
    std::map<int,int> m;
    m[3] = 9;
    oa << m;
  }
}

void load()
{
  std::ifstream file{"archive1.bin"};
  text_iarchive ia{file};
  std::map<int,int> pobjr;
  ia >> pobjr;
  std::cout<<pobjr[3]<<std::endl;
}

int main()
{
  save();
  load();
}
