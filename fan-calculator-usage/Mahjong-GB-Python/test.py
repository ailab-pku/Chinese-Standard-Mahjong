from MahjongGB import MahjongFanCalculator

print(MahjongFanCalculator((),("W1","W1","W1","W2","W2","W2","W3","W3","W3","W4","W4","W4","W5"),"W5",1,True,False,False,True,0,0))

print(MahjongFanCalculator(
    pack = (("GANG","W1",2),)
    , hand = ("W2","W2","W2","W3","W3","W3","W4","W4","W4","W5")
    , winTile = "W5"
    , flowerCount = 1
    , isSelfDrawn = False
    , is4thTile = False
    , isAboutKong = False
    , isWallLast = False
    , seatWind = 0
    , prevalentWind = 0
))

# Error
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