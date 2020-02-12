#include "MahjongGB.h"
#include <algorithm>
#include <utility>
#include <vector>
#include <string>
#include <unordered_map>
#include "../../ChineseOfficialMahjongHelper/Classes/mahjong-algorithm/fan_calculator.h"
#include <cstring>
#include <iostream>

using namespace std;

static unordered_map<string, mahjong::tile_t> str2tile;

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
    int quanFeng)
{
    vector<pair<int,string>> ans;
    mahjong::calculate_param_t calculate_param;
    mahjong::fan_table_t fan_table;
    memset(&calculate_param, 0, sizeof(mahjong::calculate_param_t));
    memset(&fan_table, 0, sizeof(mahjong::fan_table_t));
    calculate_param.hand_tiles.tile_count = hand.size();
    for(unsigned int i = 0; i < hand.size(); i++) {
        if(str2tile.find(hand[i]) == str2tile.end()){
            throw string("ERROE_WRONG_TILE_CODE");
        }
        calculate_param.hand_tiles.standing_tiles[i] = str2tile[hand[i]];
    }
    calculate_param.hand_tiles.pack_count = pack.size();
    for(unsigned int i = 0; i < pack.size(); i++) {
        pair<string, pair<string, int>> &sPack = pack[i];
        mahjong::pack_t &dPack = calculate_param.hand_tiles.fixed_packs[i];
        if(sPack.first == "PENG") {
            dPack = mahjong::make_pack(sPack.second.second, PACK_TYPE_PUNG, str2tile[sPack.second.first]);
        } else if(sPack.first == "GANG") {
            dPack = mahjong::make_pack(sPack.second.second, PACK_TYPE_KONG, str2tile[sPack.second.first]);
        } else if(sPack.first == "CHI"){
            dPack = mahjong::make_pack(sPack.second.second, PACK_TYPE_CHOW, str2tile[sPack.second.first]);
        } else {
            throw string("ERROE_WRONG_PACK_CODE");
        }
    }
    calculate_param.win_tile = str2tile[winTile];
    calculate_param.flower_count = flowerCount;
    if(isZIMO) {
        calculate_param.win_flag |= WIN_FLAG_SELF_DRAWN;
    }
    if(isLAST) {
        calculate_param.win_flag |= WIN_FLAG_WALL_LAST;
    }
    if(isJUEZHANG) {
        calculate_param.win_flag |= WIN_FLAG_4TH_TILE;
    }
    if(isGANG) {
        calculate_param.win_flag |= WIN_FLAG_ABOUT_KONG;
    }
    calculate_param.prevalent_wind = (mahjong::wind_t)quanFeng;
    calculate_param.seat_wind = (mahjong::wind_t)menFeng;
    int re = mahjong::calculate_fan(&calculate_param, &fan_table);
    if(re == -1) {
        throw string("ERROR_WRONG_TILES_COUNT");
    }else if(re == -2) {
        throw string("ERROR_TILE_COUNT_GREATER_THAN_4");
    }else if(re == -3) {
        throw string("ERROR_NOT_WIN");
    }
    for(int i = 0; i < mahjong::FAN_TABLE_SIZE; i++) {
        if(fan_table[i] > 0) {
            ans.push_back(make_pair(fan_table[i]*mahjong::fan_value_table[i],mahjong::fan_name[i]));
        }
    }
    return ans;
}

void MahjongInit()
{
    for(int i = 1; i <= 9; i++) {
        str2tile["W" + to_string(i)] = mahjong::make_tile(TILE_SUIT_CHARACTERS, i);
        str2tile["B" + to_string(i)] = mahjong::make_tile(TILE_SUIT_DOTS, i);
        str2tile["T" + to_string(i)] = mahjong::make_tile(TILE_SUIT_BAMBOO, i);
    }
    for(int i = 1; i <= 4; i++) {
        str2tile["F" + to_string((i))] = mahjong::make_tile(TILE_SUIT_HONORS, i);
    }
    for(int i = 1; i <= 3; i++) {
        str2tile["J" + to_string((i))] = mahjong::make_tile(TILE_SUIT_HONORS, i + 4);
    }
}