void handld(){
  for(int i=0;i<len, i++) {
    if(v[i]<4&&v[i]>9){
      vv.push_back(v[i]);
    }
  }


  for(auto i=v.begin();i!=v.end(); ++i){
    for(auto ii=vv.begin();ii!=vv.end(); ++ii){
      if(ii==i){
        vvv.puch_back(ii);
      }
    }
  }
};
