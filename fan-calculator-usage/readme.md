# English
ChineseOfficialMahjongHelper provides function to calculate the combination of tiles in hand.
It is forked from https://github.com/summerinsects/ChineseOfficialMahjongHelper.git

If you write AI in C++, please refer Mahjong-GB-CPP.

If you write AI in Python, please refer Mahjong-GB-Python.

Note: We have already provided these libraries (fan calculators) in Botzone runtime, and you may just `from MahjongGB import MahjongFanCalculator` or `#include "MahjongGB/MahjongGB.h"` directly in your code to submit to Botzone.

***For C++ fan calculator to work, please choose "G++ 7.2.0 with many lib" as compiler on Botzone.***

OR

If you'd rather use interfaces provided by https://github.com/summerinsects/ChineseOfficialMahjongHelper/tree/master/Classes/mahjong-algorithm , you may include cpp files as shown below (Please choose the default compiler on Botzone if this is the case):
```
#include "MahjongGB/fan_calculator.cpp"
#include "MahjongGB/shanten.cpp"
```

# 中文
ChineseOfficialMahjongHelper文件夹为国标麻将算番器。此算番器接口调用开源项目：
https://github.com/summerinsects/ChineseOfficialMahjongHelper.git

C++请参阅Mahjong-GB-CPP

Python请参阅Mahjong-GB-Python

注：Botzone内置算番库，直接from MahjongGB import MahjongFanCalculator或者#include "MahjongGB/MahjongGB.h"就可以使用算番器。

***如使用 C++ 的算番库，请在创建 Bot 时选择 "G++ 7.2.0 with many lib" 作为编译器。***

或者

如果你希望直接使用 https://github.com/summerinsects/ChineseOfficialMahjongHelper/tree/master/Classes/mahjong-algorithm 的接口，可以通过如下方式引入对应的文件（此时在 Botzone 上请使用默认编译器）：
```
#include "MahjongGB/fan_calculator.cpp"
#include "MahjongGB/shanten.cpp"
```
