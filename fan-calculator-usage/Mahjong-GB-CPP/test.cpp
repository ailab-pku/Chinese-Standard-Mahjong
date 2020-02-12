#include "MahjongGB/MahjongGB.h"
#include <iostream>
using namespace std;
int main() {
    MahjongInit();
    try{
        auto re = MahjongFanCalculator({{"GANG",{"W1",1}}},{"W2","W2","W2","W3","W3","W3","W4","W4","W4","W5"},"W5",1,0,0,0,0,0,0);
        for(auto i : re){
            cout << i.first << " " << i.second << endl;
        }
    }catch(const string &error){
        cout << error << endl;
    }
    cout << "----------" << endl;

    try{
        auto re = MahjongFanCalculator({{"GANG",{"W1",1}},{"CHI",{"T2",2}}},{"W3","W3","W3","W4","W4","W4","W5"},"W5",1,0,0,0,0,0,0);
        for(auto i : re){
            cout << i.first << " " << i.second << endl;
        }
    }catch(const string &error){
        cout << error << endl;
    }
    cout << "----------" << endl;

    //No HU
    try{
        auto re = MahjongFanCalculator({{"GANG",{"W1",1}},{"CHI",{"T2",2}}},{"W3","W3","W3","W4","W4","W4","W5"},"W7",1,0,0,0,0,0,0);
        for(auto i : re){
            cout << i.first << " " << i.second << endl;
        }
    }catch(const string &error){
        cout << error << endl;
    }
    return 0;
}