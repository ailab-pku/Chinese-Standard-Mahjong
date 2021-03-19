Mahjong Fan Calculator Python
=====

README:[English](https://github.com/ailab-pku/Chinese-Standard-Mahjong/blob/master/fan-calculator-usage/Mahjong-GB-Python/README.md)|[中文](https://github.com/ailab-pku/Chinese-Standard-Mahjong/blob/master/fan-calculator-usage/Mahjong-GB-Python/README-zh.md)

```Python
from MahjongGB import MahjongFanCalculator

# 算番函数
((fanCount, fanName), ...) MahjongFanCalculator(
    pack = ((packType, tileCode, offer), ...),
    hand = (tileCode, ...),
    winTile = tileCode,
    flowerCount = int 0..8,
    isSelfDrawn = bool,
    is4thTile = bool,
    isAboutKong = bool,
    isWallLast = bool,
    seatWind = int 0..3,
    prevalentWind = int 0..3,
	[optional, default = False]verbose = bool)
```

- pack（tuple套tuple）:玩家的明牌，每组packType（string）为"PENG" "GANG" "CHI" 三者之一，tileCode（string）为牌代码（吃牌表示中间牌代码），offer（int）碰、杠时表示上家、对家、下家供牌，吃时123表示第几张是上家供牌。
- hand（tuple）:玩家的暗牌，tileCode（string）为牌代码
- winTile（string）:和的那张牌代码
- flowerCount（int）:补花数
- isSelfDrawnbool）:是否为自摸和牌
- is4thTile（bool）:是否为和绝张
- isAboutKong（bool）:关于杠，复合点和时为枪杠和，复合自摸则为杠上开花
- isWallLast（bool）:是否为牌墙最后一张，复合自摸为妙手回春，否则为海底捞月
- seatWind（int）:门风，0123表示东南西北
- prevalentWind（int）:圈风，0123表示东南西北
- verbose（bool，默认值为False）:用来控制返回格式，如果设置为True，返回形式为每个番型的(点数、次数、中文名、英文名)
- 返回值（tuple套tuple）:每组int表示番数，求和为总番数，string是每个番形的描述