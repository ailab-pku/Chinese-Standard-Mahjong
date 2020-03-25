Mahjong Fan Calculator CPP
=====

README:[English](https://github.com/ailab-pku/Chinese-Standard-Mahjong/blob/master/fan-calculator-usage/Mahjong-GB-CPP/README.md)|[中文](https://github.com/ailab-pku/Chinese-Standard-Mahjong/blob/master/fan-calculator-usage/Mahjong-GB-CPP/README-zh.md)


***提交Bot的时候请选择 "G++ 7.2.0 with many lib"。***

```cpp
// 参考test.cpp
#include "MahjongGB/MahjongGB.h"

// 使用前初始化
void MahjongInit();

// 算番函数
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
```

- pack:玩家的明牌，每组第一个string为"PENG" "GANG" "CHI" 三者之一，第二个- string为牌代码（吃牌表示中间牌代码），第三个int碰、杠时表示上家、对家、下家供牌，吃时123表示第几张是上家供牌。
- hand:玩家的暗牌，string为牌代码
- winTile:和的那张牌代码
- flowerCount:补花数
- isZIMO:是否为自摸和牌
- isJUEZHANG:是否为和绝张
- isGANG:关于杠，复合点和时为枪杠和，复合自摸则为杠上开花
- isLast:是否为牌墙最后一张，复合自摸为妙手回春，否则为海底捞月
- menFeng:门风，0123表示东南西北
- quanFeng:圈风，0123表示东南西北
- 返回值:函数返回vector，每组int表示番数，求和为总番数，string是每个番形的描述
