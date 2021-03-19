from MahjongGB import MahjongFanCalculator

# Non-positional arguments
print(MahjongFanCalculator((),("W1","W1","W1","W2","W2","W2","W3","W3","W3","W4","W4","W4","W5"),"W5",1,True,False,False,True,0,0))

# Support keyword arguments
print(MahjongFanCalculator(
    pack = (("GANG","W1",2),)
    , hand = ("W2","W2","W2","W3","W3","W3","W4","W4","W4","W5")
    , winTile = "W5"
    , flowerCount = 2
    , isSelfDrawn = False
    , is4thTile = False
    , isAboutKong = False
    , isWallLast = False
    , seatWind = 0
    , prevalentWind = 0
))

# Support mixed arguments with unarranged keyword arguments, as well as verbose mode
print(MahjongFanCalculator(
    (("GANG","W1",2),)
    , ("W2","W2","W2","W3","W3","W3","W4","W4","W4","W5")
    , "W5"
    , prevalentWind = 0
    , seatWind = 0
    , is4thTile = False
    , isAboutKong = False
    , isSelfDrawn = False
    , isWallLast = False
    , flowerCount = 2
    , verbose = True
))

# Wrong tile count
try:
    ans = MahjongFanCalculator((),("W1","W1","W1","W2","W2","W2","W3","W3","W3","W4","W4","W4"),"W5",1,True,False,False,True,0,0)
except Exception as err:
    print(err)
else:
    print(ans)

# Not win
try:
    ans = MahjongFanCalculator((("CHI","W1",0),),("W2","W2","W2","W3","W3","W3","W4","W4","W4","W5"),"W7",1,False,False,False,False,0,0)
except Exception as err:
    print(err)
else:
    print(ans)