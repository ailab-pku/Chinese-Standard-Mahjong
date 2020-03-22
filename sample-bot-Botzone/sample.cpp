#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>

#ifdef _BOTZONE_ONLINE
#include "jsoncpp/json.h"
#else
#include <json/json.h>
#endif

#define SIMPLEIO 0
//由玩家自己定义，0表示JSON交互，1表示简单交互。

using namespace std;

vector<string> request, response;
vector<string> hand;

int main()
{
    int turnID;
    string stmp;
#if SIMPLEIO
    cin >> turnID;
    turnID--;
    getline(cin, stmp);
    for(int i = 0; i < turnID; i++) {
        getline(cin, stmp);
        request.push_back(stmp);
        getline(cin, stmp);
        response.push_back(stmp);
    }
    getline(cin, stmp);
    request.push_back(stmp);
#else
    Json::Value inputJSON;
    cin >> inputJSON;
    turnID = inputJSON["responses"].size();
    for(int i = 0; i < turnID; i++) {
        request.push_back(inputJSON["requests"][i].asString());
        response.push_back(inputJSON["responses"][i].asString());
    }
    request.push_back(inputJSON["requests"][turnID].asString());
#endif

    if(turnID < 2) {
        response.push_back("PASS");
    } else {
        int itmp, myPlayerID, quan;
        ostringstream sout;
        istringstream sin;
        sin.str(request[0]);
        sin >> itmp >> myPlayerID >> quan;
        sin.clear();
        sin.str(request[1]);
        for(int j = 0; j < 5; j++) sin >> itmp;
        for(int j = 0; j < 13; j++) {
            sin >> stmp;
            hand.push_back(stmp);
        }
        for(int i = 2; i < turnID; i++) {
            sin.clear();
            sin.str(request[i]);
            sin >> itmp;
            if(itmp == 2) {
                sin >> stmp;
                hand.push_back(stmp);
                sin.clear();
                sin.str(response[i]);
                sin >> stmp >> stmp;
                hand.erase(find(hand.begin(), hand.end(), stmp));
            }
        }
        sin.clear();
        sin.str(request[turnID]);
        sin >> itmp;
        if(itmp == 2) {
            random_shuffle(hand.begin(), hand.end());
            sout << "PLAY " << *hand.rbegin();
            hand.pop_back();
        } else {
            sout << "PASS";
        }
        response.push_back(sout.str());
    }

#if SIMPLEIO
    cout << response[turnID] << endl;
#else
    Json::Value outputJSON;
    outputJSON["response"] = response[turnID];
    cout << outputJSON << endl;
#endif
    return 0;
}
