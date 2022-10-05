from typing import Tuple
from game import Game, Phase
from random import randint
import pygame as pg
from action_dict import make_action_dict

if __name__ == "__main__":
    # does_draw = False
    does_draw = True
    g = Game(does_draw)
    num_games = 0
    try:
        while True:
            # print("---------------------------------------")
            # print(f"player: {g.player.player}")
            options = g.legal_actions()
            assert all([isinstance(x, int) for x in options])
            # print("options: ", options)
            if len(options) > 1 and g.phase in [Phase.Movement, Phase.Choose_Power]:
                action = randint(1,len(options)-1)
            else:
                action = randint(0,len(options)-1)
            # print("action: ", action)
            obs, reward, done = g.step(options[int(action)])
            # print("obs: ", obs)
            # print("reward: ", reward)
            # print("done: ", done)
            if done:
                g = Game(does_draw)
                num_games += 1
    finally:
        print(num_games)
        pg.quit()
