#include <iostream>
using namespace std;
int calc(int n);

void calc_steps(){
    while(true){
        int n;
        cin>>n;
        cout<<"total steps:"<< calc(n)<<endl;
    }
}
int calc(int n){
    if (n==1){
        return 1;
    }
    else if(n==2){
        return 2;
    }
    return calc(n-2)+calc(n-1);
}
int main(){
    calc_steps();
}
