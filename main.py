from game.game import Game
import pygame as pg
import players.random_player as randplayer

if __name__ == "__main__":
    does_draw = False
    # does_draw = True
    should_print = False
    g = Game(does_draw)
    num_games = 0
    p1 = randplayer.choose_action
    p2 = randplayer.choose_action
    obs = None
    try:
        while True:
            if should_print: print("---------------------------------------")
            if should_print: print(f"player: {g.player.player}")
            options = g.legal_actions()
            if g.to_play() == 1:
                action = p1(options, obs)
            elif g.to_play() == 2:
                action = p2(options, obs)
            if should_print: print("options: ", options)
            if should_print: print("action: ", action)
            obs, reward, done = g.step(options[action])
            if should_print: print("obs: ", obs)
            if should_print: print("reward: ", reward)
            if should_print: print("done: ", done)
            if done:
                g = Game(does_draw)
                num_games += 1
    finally:
        print(num_games)
        pg.quit()
