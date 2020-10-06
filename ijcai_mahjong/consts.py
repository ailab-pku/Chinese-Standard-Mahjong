# -*- coding:utf-8 -*-
from enum import Enum

NUM_PLAYERS = 4
NUM_HAND_TILES = 13


# 风圈
class RoundWind(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


class TileSuit(Enum):
    CHARACTERS = 1  # 万
    BAMBOO = 2      # 条
    DOTS = 3        # 饼
    HONORS = 4      # 字


class ActionType(Enum):
    PASS = 0       # 无操作
    DRAW = 1       # 摸牌
    PLAY = 2       # 打牌
    CHOW = 3       # 吃牌
    PUNG = 4       # 碰牌
    KONG = 5       # 杠牌
    MELD_KONG = 6  # 补杠
    HU = 7         # 和牌


class ClaimingType:
    CHOW = "CHI"
    PUNG = "PENG"
    KONG = "GANG"
