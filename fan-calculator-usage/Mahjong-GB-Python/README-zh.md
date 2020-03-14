Mahjong Fan Calculator Python
=====

README:[English](https://github.com/ailab-pku/Chinese-Standard-Mahjong/blob/master/fan-calculator-usage/Mahjong-GB-Python/README.md)|[中文](https://github.com/ailab-pku/Chinese-Standard-Mahjong/blob/master/fan-calculator-usage/Mahjong-GB-Python/README-zh.md)

```Python
from MahjongGB import MahjongFanCalculator

# 算番函数
((value,descripthon),...) MahjongFanCalculator(
    pack=((packType,tileCode,data),...),
    hand=(tileCode,...),
    winTile,
    flowerCount,
    isZIMO,
    isJUEZHANG,
    isGANG,
    isLAST,
    menFeng,
    quanFeng)
```

- pack（tuple套tuple）:玩家的明牌，每组packType（string）为"PENG" "GANG" "CHI" 三者之一，tileCode（string）为牌代码（吃牌表示中间牌代码），data（int）碰、杠时表示上家、对家、下家供牌，吃时123表示第几张是上家供牌。
- hand（tuple）:玩家的暗牌，tileCode（string）为牌代码
- winTile（string）:和的那张牌代码
- flowerCount（int）:补花数
- isZIMO（bool）:是否为自摸和牌
- isJUEZHANG（bool）:是否为和绝张
- isGANG（bool）:关于杠，复合点和时为枪杠和，复合自摸则为杠上开花
- isLast（bool）:是否为牌墙最后一张，复合自摸为妙手回春，否则为海底捞月
- menFeng（int）:门风，0123表示东南西北
- quanFeng（int）:圈风，0123表示东南西北
- 返回值（tuple套tuple）:每组int表示番数，求和为总番数，string是每个番形的描述