Mahjong Fan Calculator Python
=====

README:[English](https://github.com/ailab-pku/Chinese-Standard-Mahjong/blob/master/fan-calculator-usage/Mahjong-GB-Python/README.md)|[中文](https://github.com/ailab-pku/Chinese-Standard-Mahjong/blob/master/fan-calculator-usage/Mahjong-GB-Python/README-zh.md)

```Python
from MahjongGB import MahjongFanCalculator

# Fan calculator
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
    prevalentWind = int 0..3)
```

- pack: The declared tiles. A tuple of tuples of three elements each: packType of "PENG"/"GANG"/"CHI", tileCode and offer. Click [here](https://github.com/ailab-pku/Chinese-Standard-Mahjong/blob/master/fan-calculator-usage/ChineseOfficialMahjongHelper/Classes/mahjong-algorithm/README.md) for details.
- hand: The concealed tiles in hand. A tuple of tileCodes.
- winTile: The winning tile to make Mahjong.
- flowerCount: The number of the Flower and Season tiles.
- isSelfDrawn: Whether the winning tile is self drawn.
- is4thTile: Whether the winning tile is the 4th tile.
- isAboutKong: Whether the winning is about Kong. If the player wins by other's discard, it is Robbing the Kong. Otherwise, if the player wins by self-drawn, it is Out with Replacement Tile.
- isWallLast: Whether the winning tile is the last one in tile wall. If self-drawn, it is Last Tile Draw. Otherwise, it is Last Tile Claim.
- seatWind: Seat wind. The number 0, 1, 2, 3 represent East, South, West, and North respectively.
- prevalentWind: Prevalent wind. The number 0, 1, 2, 3 represent East, South, West, and North respectively.
- return: This function returns a tuple of tuples of two elements each: the fan count and fan name of each fan.