#ifndef MAHJONG_H
#define MAHJONG_H

#include <utility>
#include <vector>
#include <string>

//CPP
#include "MahjongGB.cpp"
#include "../../ChineseOfficialMahjongHelper/Classes/mahjong-algorithm/fan_calculator.cpp"
#include "../../ChineseOfficialMahjongHelper/Classes/mahjong-algorithm/shanten.cpp"
//Dangerous

using namespace std;

void MahjongInit();

vector<pair<int, string> > MahjongFanCalculator(
    vector<pair<string, pair<string, int> > > pack,
    vector<string> hand,
    string winTile,
    int flowerCount,
    bool isZIMO,
    bool isJUEZHANG,
    bool isGANG,
    bool isLAST,
    int menFeng,
    int quanFeng);

#endif
