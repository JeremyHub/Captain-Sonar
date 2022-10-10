from game.game import Game
import pygame as pg
import players.random_player as randplayer

if __name__ == "__main__":
    does_draw = False
    # does_draw = True
    g = Game(does_draw)
    num_games = 0
    p1 = randplayer.choose_action
    p2 = randplayer.choose_action
    obs = None
    try:
        while True:
            # print("---------------------------------------")
            # print(f"player: {g.player.player}")
            options = g.legal_actions()
            if g.to_play() == 1:
                action = p1(options, obs)
            elif g.to_play() == 2:
                action = p2(options, obs)
            # print("options: ", options)
            # print("action: ", action)
            obs, reward, done = g.step(options[action])
            # print("obs: ", obs)
            # print("reward: ", reward)
            # print("done: ", done)
            if done:
                g = Game(does_draw)
                num_games += 1
    finally:
        print(num_games)
        pg.quit()
