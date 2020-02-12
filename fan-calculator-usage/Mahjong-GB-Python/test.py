from MahjongGB import MahjongFanCalculator

try:
    ans=MahjongFanCalculator((),("W1","W1","W1","W2","W2","W2","W3","W3","W3","W4","W4","W4","W5"),"W5",1,True,False,False,True,0,0)
except Exception as err:
    print(err)
else:
    print(ans)

try:
    ans=MahjongFanCalculator((("GANG","W1",2),),("W2","W2","W2","W3","W3","W3","W4","W4","W4","W5"),"W5",1,False,False,False,False,0,0)
except Exception as err:
    print(err)
else:
    print(ans)

#错误
try:
    ans=MahjongFanCalculator((),("W1","W1","W1","W2","W2","W2","W3","W3","W3","W4","W4","W4"),"W5",1,True,False,False,True,0,0)
except Exception as err:
    print(err)
else:
    print(ans)

#没和
try:
    ans=MahjongFanCalculator((("CHI","W1",0),),("W2","W2","W2","W3","W3","W3","W4","W4","W4","W5"),"W7",1,False,False,False,False,0,0)
except Exception as err:
    print(err)
else:
    print(ans)