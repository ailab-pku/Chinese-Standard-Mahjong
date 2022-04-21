# -*- coding:utf-8 -*-
from typing import List, Tuple

from ijcai_mahjong import consts


class Claiming:
    def __init__(self, claiming_type: int, tile: str, data: int):
        self.claiming_type = claiming_type
        self.tile = tile
        self.data = data


class PlayerData:
    def __init__(self, index: int):
        self.index = index
        self.tile_wall = []  # type: List[str]
        self.tiles = []      # type: List[str]
        self.claimings = []  # type: List[Claiming]

    @property
    def claimings_and_tiles(self):
        claimings = []
        for claiming in self.claimings:
            if claiming.claiming_type == consts.ClaimingType.CHOW:
                data = claiming.data
            else:
                data = (claiming.data - self.index + consts.NUM_PLAYERS) % consts.NUM_PLAYERS
            claimings.append((claiming.claiming_type, claiming.tile, data))
        return tuple(claimings), tuple(self.tiles)

    def play(self, tile: str) -> bool:
        if tile not in self.tiles:
            return False
        self.tiles.remove(tile)
        return True

    def pung(self, tile: str, offer_player: int) -> bool:
        if self.tiles.count(tile) < 2:
            return False
        for _ in range(2):
            self.tiles.remove(tile)
        self.claimings.append(Claiming(consts.ClaimingType.PUNG, tile, offer_player))
        return True

    def kong(self, tile: str, data: int) -> bool:
        if self.tiles.count(tile) < 4:
            return False
        for _ in range(4):
            self.tiles.remove(tile)
        self.claimings.append(Claiming(consts.ClaimingType.KONG, tile, data))
        return True

    def meld_kong(self, tile: str) -> bool:
        claiming_index = -1
        for i in range(len(self.claimings)):
            claiming = self.claimings[i]
            if claiming.claiming_type == consts.ClaimingType.PUNG and claiming.tile == tile:
                claiming_index = i
                break
        if claiming_index == -1:
            return False
        if tile not in self.tiles:
            return False
        self.tiles.remove(tile)
        self.claimings[claiming_index].claiming_type = consts.ClaimingType.KONG
        return True

    def chow(self, tiles: List[str], data: int) -> bool:
        for tile in tiles:
            if tile not in self.tiles:
                return False
        for tile in tiles:
            self.tiles.remove(tile)
        self.claimings.append(Claiming(consts.ClaimingType.CHOW, tiles[1], data))
        return True
