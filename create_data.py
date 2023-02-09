from .game.game import CaptainSonar
from .game.observation import Observation, Public_Actions
from .actors.expert_actor import Expert_Actor
import multiprocessing as mp
import pandas as pd

def save_one_game_actions(game_num):
    g = CaptainSonar(False)
    obs = g.reset()
    p1 = Expert_Actor(g.ACTION_DICT, g.REVERSE_ACTION_DICT, g.board)
    p2 = Expert_Actor(g.ACTION_DICT, g.REVERSE_ACTION_DICT, g.board)
    done = False
    actions = []
    while not done:
        options = g.legal_actions()
        if g.to_play() == 0:
            action = p1.choose_action(options, obs)
            actions.append((obs, action))
            was_p1 = True
        elif g.to_play() == 1:
            was_p1 = False
            action = p2.choose_action(options, obs)
            actions.append((obs, action))
        obs, reward, done = g.step(action)
    if game_num % 100 == 0:
        print(f"game {game_num} done")
    return actions

def main():
    num_games = 100

    actions = []
    pool = mp.Pool(processes=mp.cpu_count())
    map_result = pool.map_async(save_one_game_actions, [i for i in range(num_games)])
    result_log = map_result.get()
    pool.close()

    for game_actions in result_log:
        actions.extend(game_actions)

    df = pd.DataFrame(actions)
    df.to_csv("Captain-Sonar/actions.csv")

if __name__ == "__main__":
    main()