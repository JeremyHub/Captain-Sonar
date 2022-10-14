from game.game import Game
import pygame as pg
import players.random_player as randplayer
import players.expert_player as explayer

if __name__ == "__main__":
    does_draw = False
    # does_draw = True
    should_print = False
    g = Game(does_draw)
    num_games = 0
    p1 = randplayer.choose_action
    p1_total_dmg = 0
    p2 = explayer.choose_action
    p2_total_dmg = 0
    obs = None
    try:
        while True:
            if should_print: print("---------------------------------------")
            if should_print: print(f"player: {g.player.player}")
            options = g.legal_actions()
            if g.to_play() == 1:
                action = p1(options, obs)
            elif g.to_play() == 2:
                action = p2(options, obs, g.ACTION_DICT, g.REVERSE_ACTION_DICT)
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
