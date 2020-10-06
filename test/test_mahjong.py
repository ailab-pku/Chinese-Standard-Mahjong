# -*- coding:utf-8 -*-
from ijcai_mahjong import consts
from ijcai_mahjong.core import Mahjong


def init() -> Mahjong:
    print()
    env = Mahjong()
    print("init")
    for i in range(consts.NUM_PLAYERS):
        print(f"player[{i}]: {env.observation(i)}, round_stage[{env.round_stage}]")
    return env


def step(env: Mahjong, actions: list):
    print()
    env.step(actions)
    print(f"actions: {actions}")
    for i in range(consts.NUM_PLAYERS):
        print(f"player[{i}]: {env.observation(i)}, round_stage[{env.round_stage}]")


def test_false_hu():
    env = init()
    actions = [(consts.ActionType.HU.value, None), (consts.ActionType.PASS.value, None),
               (consts.ActionType.PASS.value, None), (consts.ActionType.PASS.value, None)]
    step(env, actions)
    print()
    print(f"done: {env.done}")
    print(f"reward: {env.rewards}")
    assert env.done, True
    assert env.rewards, {"0": -30, "1": 10, "2": 10, "3": 10}


def test_true_hu():
    env = init()
    # 0 play W8
    actions = [(consts.ActionType.PLAY.value, "F1"), (consts.ActionType.PASS.value, None),
               (consts.ActionType.PASS.value, None), (consts.ActionType.PASS.value, None)]
    step(env, actions)

    # 1 pung and play F2
    actions = [(consts.ActionType.PASS.value, None), (consts.ActionType.PUNG.value, "F2"),
               (consts.ActionType.PASS.value, None), (consts.ActionType.PASS.value, None)]
    step(env, actions)

    # all pass
    actions = [(consts.ActionType.PASS.value, None), (consts.ActionType.PASS.value, None),
               (consts.ActionType.PASS.value, None), (consts.ActionType.PASS.value, None)]
    step(env, actions)

    # 2 play W4
    actions = [(consts.ActionType.PASS.value, None), (consts.ActionType.PASS.value, None),
               (consts.ActionType.PLAY.value, "W4"), (consts.ActionType.PASS.value, None)]
    step(env, actions)

    # 3 chow W4
    actions = [(consts.ActionType.PASS.value, None), (consts.ActionType.PASS.value, None),
               (consts.ActionType.PASS.value, None), (consts.ActionType.CHOW.value, "W3 W3")]
    step(env, actions)

    # all pass
    actions = [(consts.ActionType.PASS.value, None), (consts.ActionType.PASS.value, None),
               (consts.ActionType.PASS.value, None), (consts.ActionType.PASS.value, None)]
    step(env, actions)

    # cheat, let 0 hu 😂
    env.players_data[0].tiles = ["W1", "W1", "W1", "W2", "W2", "W2", "W3", "W3", "W3", "W4", "W4", "W4", "W5"]
    env.last_tile = "W5"
    actions = [(consts.ActionType.HU.value, None), (consts.ActionType.PASS.value, None),
               (consts.ActionType.PASS.value, None), (consts.ActionType.PASS.value, None)]
    step(env, actions)

    print()
    print(f"done: {env.done}")
    print(f"reward: {env.rewards}")
    assert env.done, True
    assert env.rewards, {"0": 438, "1": -146, "2": -146, "3": -146}
