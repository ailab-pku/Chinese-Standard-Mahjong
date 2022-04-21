# -*- coding:utf-8 -*-
import random
import sys
from typing import Any, List, Tuple

from MahjongGB import MahjongFanCalculator

from ijcai_mahjong import consts
from ijcai_mahjong.player_data import PlayerData


class Mahjong:
    def __init__(self, random_seed: int = 42):
        self.random_seed = random_seed
        random.seed(self.random_seed)

        self.round_wind = self.__generate_round_wind()
        tile_wall = self.__generate_tile_wall()
        self.players_data = self.__deal(tile_wall)
        self.done, self.rewards = False, {str(i): 0 for i in range(consts.NUM_PLAYERS)}
        self.round_stage, self.last_round_stage = 0, None
        self.last_action, self.last_operation = None, None
        self.current_exposed_kung = self.current_concealed_kung = self.current_meld_kung = \
            self.last_exposed_kung = self.last_concealed_kung = self.last_meld_kung = False
        self.played_tiles = {tile: 0 for tile in set([t for t in tile_wall])}
        self.last_tile = self.__draw_tile()
        self.rewards = {}

    def reset(self):
        self.random_seed = random.randint(0, sys.maxsize)
        random.seed(self.random_seed)

        self.round_wind = self.__generate_round_wind()
        tile_wall = self.__generate_tile_wall()
        self.players_data = self.__deal(tile_wall)
        self.done, self.rewards = False, {str(i): 0 for i in range(consts.NUM_PLAYERS)}
        self.round_stage, self.last_round_stage = 0, None
        self.last_operation = None
        self.current_exposed_kung = self.current_concealed_kung = self.current_meld_kung = \
            self.last_exposed_kung = self.last_concealed_kung = self.last_meld_kung = False
        self.played_tiles = {tile: 0 for tile in set([t for t in tile_wall])}
        self.last_tile = self.__draw_tile()

    def observation(self, player: int) -> dict:
        return {
            "tiles": " ".join(sorted(self.players_data[player].tiles)),
            "claimings": ";".join([f"{claiming.claiming_type} {claiming.tile} {claiming.data}"
                                   for claiming in self.players_data[player].claimings]),
            "tile_wall_count": len(self.players_data[player].tile_wall),
            "draw_tile": self.last_tile if (player == self.round_stage and 0 <= self.round_stage < 4) else None,
            "last_action": self.last_action,
        }

    @staticmethod
    def __generate_round_wind() -> int:
        return random.choice([consts.RoundWind.EAST, consts.RoundWind.SOUTH,
                              consts.RoundWind.WEST, consts.RoundWind.NORTH]).value

    @staticmethod
    def __generate_tile_wall() -> List[str]:
        tile_wall = list()
        # 数牌(万, 条, 饼), 风牌, 箭牌
        for _ in range(4):
            for i in range(1, 9 + 1):
                tile_wall.append(f"W{i}")
                tile_wall.append(f"T{i}")
                tile_wall.append(f"B{i}")
            for i in range(1, 4 + 1):
                tile_wall.append(f"F{i}")
            for i in range(1, 3 + 1):
                tile_wall.append(f"J{i}")
        random.shuffle(tile_wall)
        return tile_wall

    @staticmethod
    def __deal(tile_wall: List[str]) -> List[PlayerData]:
        players_data = [PlayerData(i) for i in range(consts.NUM_PLAYERS)]
        num_init_cards = len(tile_wall) // consts.NUM_PLAYERS
        for i in range(consts.NUM_PLAYERS):
            for j in range(num_init_cards):
                players_data[i].tile_wall.append(tile_wall[i * num_init_cards + j])
        for i in range(consts.NUM_PLAYERS):
            for _ in range(consts.NUM_HAND_TILES):
                players_data[i].tiles.append(players_data[i].tile_wall.pop())
        return players_data

    def __win(self, player: int, fan: int):
        self.done = True
        self.rewards = {p: 0 for p in range(consts.NUM_PLAYERS)}
        for i in range(consts.NUM_PLAYERS):
            if self.round_stage < 4:
                if i == player:
                    self.rewards[i] = 3 * (8 + fan)
                else:
                    self.rewards[i] = -(8 + fan)
            else:
                if i == player:
                    self.rewards[i] = 3 * (8 + fan)
                elif self.round_stage == i + 4:
                    self.rewards[i] = -(8 + fan)
                elif self.round_stage == i + 8 and (self.last_meld_kung or self.last_concealed_kung):
                    self.rewards[i] = -(8 + fan)
                else:
                    self.rewards[i] = -8

    def __lose(self, player: int):
        self.done = True
        self.rewards = {p: 10 if p != player else -30 for p in range(consts.NUM_PLAYERS)}

    def __huang(self):
        self.done = True
        self.rewards = {p: 0 for p in range(consts.NUM_PLAYERS)}

    def __check_pass(self, player: int, action: Tuple[int, Any]) -> bool:
        action_type, _ = action
        if action_type != consts.ActionType.PASS.value:
            self.__lose(player)
            return False
        return True

    def __check_draw(self, player: int, action: Tuple[int, Any]) -> bool:
        action_type, action_content = action
        if action_type == consts.ActionType.HU.value:
            fan = self.__calculate_fan(player)
            self.__lose(player) if fan < 8 else self.__win(player, fan)
            return False
        elif action_type in {consts.ActionType.PLAY.value, consts.ActionType.KONG.value,
                             consts.ActionType.MELD_KONG.value}:
            self.players_data[player].tiles.append(self.last_tile)
            self.last_tile = action_content
            if action_type == consts.ActionType.PLAY.value:
                if self.players_data[player].play(action_content) is True:
                    self.last_operation = consts.ActionType.PLAY.value
                    self.round_stage += 4
                    return True
            elif action_type == consts.ActionType.KONG.value:
                if len(self.players_data[player].tile_wall) == 0 or \
                        len(self.players_data[(player + 1) % consts.NUM_PLAYERS].tiles) == 0:
                    self.__lose(player)
                    return False
                if self.players_data[player].kong(self.last_tile, player) is True:
                    self.last_operation = consts.ActionType.KONG.value
                    self.current_concealed_kung = True
                    self.current_exposed_kung = self.last_exposed_kung = self.current_meld_kung = self.last_meld_kung = False
                    self.round_stage = player + 8
                    return True
            elif action_type == consts.ActionType.MELD_KONG.value:
                if len(self.players_data[player].tile_wall) == 0 or \
                        len(self.players_data[(player + 1) % consts.NUM_PLAYERS].tiles) == 0:
                    self.__lose(player)
                    return False
                if self.players_data[player].meld_kong(self.last_tile) is True:
                    self.played_tiles[self.last_tile] = 4
                    self.last_operation = consts.ActionType.MELD_KONG.value
                    self.current_meld_kung = True
                    self.current_concealed_kung = self.last_concealed_kung = self.current_exposed_kung = self.last_exposed_kung = False
                    self.round_stage = player + 8
                    return True
        self.__lose(player)
        return False

    def __check_hu(self, player: int, action: Tuple[int, Any]) -> bool:
        action_type, _ = action
        if action_type == consts.ActionType.HU.value:
            fan = self.__calculate_fan(player)
            self.__lose(player) if fan < 8 else self.__win(player, fan)
            return False
        return True

    def __check_pung_kong(self, player: int, action: Tuple[int, Any]) -> bool:
        action_type, action_content = action
        if action_type == consts.ActionType.PASS.value:
            return True
        elif action_type == consts.ActionType.KONG.value:
            if self.players_data[player].kong(self.last_tile, self.round_stage % 4) is False:
                self.__lose(player)
                return False
            self.played_tiles[self.last_tile] = 4
            self.last_operation = consts.ActionType.KONG.value
            self.current_exposed_kung = True
            self.last_meld_kung = self.current_meld_kung = self.last_concealed_kung = self.current_concealed_kung = False
            self.round_stage = player + 8
        elif action_type == consts.ActionType.PUNG.value:
            if self.players_data[player].pung(self.last_tile, self.round_stage % 4) is False:
                self.__lose(player)
                return False
            self.played_tiles[self.last_tile] += 3
            self.last_operation = consts.ActionType.PUNG.value
            self.last_tile = action_content
            if self.players_data[player].play(action_content) is False:
                self.__lose(player)
                return False
            self.round_stage = player + 4
            return False
        elif action_type != consts.ActionType.CHOW.value:
            self.__lose(player)
            return False
        return True

    def __check_chow(self, player: int, action: Tuple[int, Any]) -> bool:
        action_type, action_content = action
        if action_type != consts.ActionType.CHOW.value:
            return True

        if (self.round_stage - player) % consts.NUM_PLAYERS != 3:
            self.__lose(player)
            return False
        chow_tiles_middle, play_tile = action_content.split()
        if chow_tiles_middle[0] not in {"W", "B", "T"} or chow_tiles_middle[0] != self.last_tile[0] or abs(
                int(self.last_tile[1]) - int(chow_tiles_middle[1])) > 1:
            self.__lose(player)
            return False
        self.players_data[player].tiles.append(self.last_tile)
        suit, number = chow_tiles_middle
        chow_tiles = [f"{suit}{int(number) - 1}", chow_tiles_middle, f"{suit}{int(number) + 1}"]
        chow_tile_index = 0
        for i in range(len(chow_tiles)):
            if self.last_tile == chow_tiles[i]:
                chow_tile_index = i + 1
                break
        if self.players_data[player].chow(chow_tiles, chow_tile_index) is False:
            self.__lose(player)
            return False
        self.last_operation = consts.ActionType.CHOW.value
        self.last_tile = play_tile
        if self.players_data[player].play(play_tile) is False:
            self.__lose(player)
            return False
        self.round_stage = player + 4
        return False

    def __check_kong(self, player: int, action: Tuple[int, Any]) -> bool:
        action_type, _ = action
        if action_type == consts.ActionType.PASS:
            return True
        if self.last_meld_kung is True and self.round_stage % consts.NUM_PLAYERS != player and action_type == consts.ActionType.HU:
            fan = self.__calculate_fan(player)
            self.__lose(player) if fan < 8 else self.__win(player, fan)
            return False
        self.__lose(player)
        return False

    def step(self, actions: List[Tuple[int, Any]]):
        self.last_round_stage = self.round_stage
        self.last_action = ";".join([f"{action[0]}{' ' + action[1] if action[1] is not None else ''}" for action in actions])
        if 0 <= self.round_stage < 4:
            for i in range(consts.NUM_PLAYERS):
                if self.round_stage != i:
                    if self.__check_pass(i, actions[i]) is False:
                        break
                else:
                    if self.__check_draw(i, actions[i]) is False:
                        break
                    self.last_exposed_kung = self.current_exposed_kung
                    self.last_concealed_kung = self.current_concealed_kung
                    self.last_meld_kung = self.current_meld_kung
                    self.current_exposed_kung = self.current_concealed_kung = self.current_meld_kung = False
        elif 4 <= self.round_stage < 8:
            for i in range(consts.NUM_PLAYERS):
                if i == 0:
                    if self.__check_pass(self.round_stage % consts.NUM_PLAYERS,
                                         actions[self.round_stage % consts.NUM_PLAYERS]) is False:
                        break
                else:
                    if self.__check_hu((self.round_stage + i) % consts.NUM_PLAYERS,
                                       actions[(self.round_stage + i) % consts.NUM_PLAYERS]) is False:
                        break

            pass_flag = True

            for i in range(consts.NUM_PLAYERS):
                if pass_flag is True and self.round_stage != i + 4:
                    pass_flag = self.__check_pung_kong(i, actions[i])

            for i in range(consts.NUM_PLAYERS):
                if pass_flag is True and self.round_stage != i + 4:
                    pass_flag = self.__check_chow(i, actions[i])

            if pass_flag is True:
                self.round_stage = (self.round_stage + 1) % consts.NUM_PLAYERS
                self.played_tiles[self.last_tile] += 1
        else:
            for i in range(consts.NUM_PLAYERS):
                if self.__check_hu((self.round_stage + i) % consts.NUM_PLAYERS,
                                   actions[(self.round_stage + i) % consts.NUM_PLAYERS]) is False:
                    break
            if not self.done:
                self.round_stage -= 8

        if 0 <= self.round_stage < 4:
            if len(self.players_data[self.round_stage % consts.NUM_PLAYERS].tile_wall) == 0:
                self.__huang()
            else:
                self.last_tile = self.__draw_tile()
        elif 4 <= self.round_stage < 8:
            if len(self.players_data[(self.last_round_stage + 1) % consts.NUM_PLAYERS].tile_wall) == 0 and \
                    self.last_operation in {consts.ActionType.CHOW.value, consts.ActionType.PUNG.value}:
                self.__lose(self.round_stage % consts.NUM_PLAYERS)
        else:
            if len(self.players_data[(self.last_round_stage + 1) % consts.NUM_PLAYERS].tile_wall) == 0 and \
                    self.last_operation in {consts.ActionType.KONG.value, consts.ActionType.MELD_KONG.value}:
                self.__lose(self.round_stage % consts.NUM_PLAYERS)

    def __calculate_fan(self, player: int) -> int:
        claimings, tiles = self.players_data[player].claimings_and_tiles  # 明牌, 暗牌
        win_tile = self.last_tile  # 和牌
        flower_count = 0  # 补花数
        is_self_draw = player == self.round_stage  # 自摸
        is_fourth_tile = self.played_tiles[self.last_tile] == 3  # 绝张
        is_kong = self.last_meld_kung or self.last_concealed_kung or self.current_meld_kung  # 杠
        is_last_tile = len(self.players_data[(self.round_stage + 1) % consts.NUM_PLAYERS].tile_wall) == 0  # 牌墙最后一张
        player_wind = player  # 门风
        round_wind = self.round_wind  # 圈风

        try:
            result = MahjongFanCalculator(claimings, tiles, win_tile, flower_count, is_self_draw, is_fourth_tile,
                                          is_kong, is_last_tile, player_wind, round_wind)
            return sum([res[0] for res in result])
        except Exception as exception:
            if str(exception) == "ERROR_NOT_WIN":
                return -1
            raise

    def __draw_tile(self) -> str:
        self.last_operation = consts.ActionType.DRAW.value
        return self.players_data[self.round_stage].tile_wall.pop()

