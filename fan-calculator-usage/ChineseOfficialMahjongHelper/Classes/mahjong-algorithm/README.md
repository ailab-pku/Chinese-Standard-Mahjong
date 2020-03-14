Mahjong-algorithm
=========

README:[English](https://github.com/ailab-pku/Chinese-Standard-Mahjong/blob/master/fan-calculator-usage/ChineseOfficialMahjongHelper/Classes/mahjong-algorithm/README.md)|[中文](https://github.com/ailab-pku/Chinese-Standard-Mahjong/blob/master/fan-calculator-usage/ChineseOfficialMahjongHelper/Classes/mahjong-algorithm/README-zh.md)

## Introduction
Though written in C++, the code doesn't contain STL. It is easy to use in other languages.
- fan_calculator
  - calculate the combination of tiles in hand.
- shanten: 
  - check whether the player is waiting to win.
  - calculate which tiles can make Mahjong.
  - calculate the distance to making Mahjong.
  - calculate which tiles in hand are effective.
- stringify: 
  - string convertion.
- For more details, please read unit_test.cpp.

## Terminology 
- Claiming a tile
  - Sequence / Chow: 3 consecutive tiles of the same suit, like < Dot 2, Dot3, Dot 4 >.
  - Pung: The same 3 tiles of the same kind.
  - Kong: The same 4 tiles of the same kind. The exposed Kong uses the tile discarded by others. The concealed Kong means that one has the same 4 tiles, and it belongs to Concealed hand introduced below.
- Concealed hand: No Chow, Pung or exposed Kong.
- Meld: The collective name of Sequence, Pung and Kong. 
- Pair: The same 2 tiles of the same kind.
- Basic combination: 4 Melds and 1 pair.
- Special combination: Seven Pairs, Thirteen Orphans, Lesser Honours and Knitted Tiles, etc.
- Tiles in hand: The tiles excluding declared chows, pungs, and kongs.
- All hand tiles: All the tiles owned by the player, including declared chows, pungs, and kongs.
- Ready hand / Waiting to win: The distance between all hand tiles and winning hands.
- N shanten: Change N tiles, the hand tiles is waiting to win.
- Effective tiles: The tiles which could decrease the number of shanten.
- Improved tiles: The tiles which could increase the number of effective tiles.


## Stringify
 - Suits: Character=m, Bamboo=s, Dot=p. In this tool we use lowercase character as suffic. If a series of tiles are of the same suit, we can simplify 1m2m3m as 123m.
 - Direction/Wind and Cardinal Tiles: 
    - East=E / 1z, South=S / 2z, West=W / 3z, North=N / 4z.  
    - Red Dragon=C / 5z, Green Dragon=F / 6z, White Dragon=P / 7z.
 - Chow: The player can only chows the opponent in the left. We use \[567m,2\] to represent the player forming a sequence of 5m, 6m, and 7m. 2 represents that the 6m is the tile discarded in the last turn. If there is no 2, the default discard is the first tile, i.e., 5m.
 - Pung: We use \[999s,3\] to represent that the player forms a pung of 9s by the tile discarded by the opponent in the right (the number 3). Number 2 refers to the opponent in the opposite, and number 1 refers to the opponent in the left. The default number is 1.
 - Kong: It is similar as Pung.However, if there is no specific number, it is be considered as a concealed kong. E.g., \[SSSS\] represents a concealed kong of South. \[8888p,1\] represents forming a exposed kong by the 8p discarded by the opponent in the left. When the number is 5/6/7, it means pung to kong. E.g., \[1111s,6\] represents that the player formed a pung of 1s by the discard from the opponent in the opposite, and in the following turn, he draws the 4th 1s and decides to change the declared pung to kong.
 - Examples:
   - \[EEEE\]\[CCCC\]\[FFFF\]\[PPPP\]NN
   - 1112345678999s9s
   - \[WWWW,1\]\[444s\]45m678pFF6m
   - \[EEEE\]288s349pSCFF2p
   - \[123p,1\]\[345s,2\]\[999s,3\]6m6pEW1m
   - 356m18s1579pWNFF9p
