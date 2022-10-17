from game.breakdowns import BreakdownMap
from game.game import Game
import pygame as pg
from game.observation import Observation, Public_Actions
from actors.random_actor import Random_Actor
from actors.expert_actor import Expert_Actor

if __name__ == "__main__":
    does_draw = False
    # does_draw = True
    should_print = False
    g = Game(does_draw)
    num_games = 0
    p1 = Random_Actor(g.ACTION_DICT, g.REVERSE_ACTION_DICT)
    p1_total_dmg = 0
    p2 = Expert_Actor(g. ACTION_DICT, g.REVERSE_ACTION_DICT)
    p2_total_dmg = 0
    obs = g._update_observation(Observation(Public_Actions())).get_obs_arr()
    prev_num = -1
    try:
        while True:
            if not num_games % 100 and not num_games == prev_num:
                print(num_games)
                prev_num = num_games
            if should_print: print("---------------------------------------")
            if should_print: print(f"player: {g.player.player}")
            options = g.legal_actions()
            if g.to_play() == 1:
                action = p1.choose_action(options, obs)
            elif g.to_play() == 2:
                action = p2.choose_action(options, obs)
            if should_print: print("phase: ", g.phase)
            if should_print: print("options: ", options)
            if should_print: print("action: ", action)
            obs, reward, done = g.step(options[action])
            if should_print: print("obs: ", obs)
            if should_print: print("reward: ", reward)
            if should_print: print("done: ", done)
            if done:
                p1_total_dmg += g.p1.damage
                p2_total_dmg += g.p2.damage
                g = Game(does_draw)
                num_games += 1
    finally:
        print(num_games)
        print("p1 total dmg: ", p1_total_dmg)
        print("p2 total dmg: ", p2_total_dmg)
        print("ratio: ", p1_total_dmg/p2_total_dmg)
        pg.quit()
