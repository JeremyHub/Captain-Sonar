from .game.game import CaptainSonar, Phase
from .game.game_only_move_steps import Game_Only_Move_Steps
from .game.observation import Observation, Public_Actions
from .actors.random_actor import Random_Actor
from .actors.expert_actor import Expert_Actor
from .actors.human_actor import Human_Actor
import multiprocessing as mp


def run_one_game(tuple_of_args):
    does_draw, should_print, actor1, actor2, game_num, game_type = tuple_of_args
    g = game_type(does_draw)
    obs = g.reset()
    p1 = actor1(g.ACTION_DICT, g.REVERSE_ACTION_DICT, g.board)
    p1_rewards = []
    p2 = actor2(g.ACTION_DICT, g.REVERSE_ACTION_DICT, g.board)
    p2_rewards = []
    done = False
    num_turns = 0
    while not done:
        if should_print: print("---------------------------------------")
        if should_print: print("player: ", g.player.player)
        options = g.legal_actions()
        if g.to_play() == 0:
            action = p1.choose_action(options, obs)
            was_p1 = True
        elif g.to_play() == 1:
            was_p1 = False
            action = p2.choose_action(options, obs)
        if should_print: print("phase: ", g.phase)
        if should_print: print("options: ", options)
        if should_print: print("action: ", g.REVERSE_ACTION_DICT[action])
        obs, reward, done = g.step(action)
        if was_p1:
            p1_rewards.append(reward)
        else:
            p2_rewards.append(reward)
        if g.phase == Phase.Movement:
            num_turns += 1
        if does_draw:
            g.pg_draw_points(p1.possible_opp_positions, (255,255,255), 10)
            g.pg_draw_points([p1.average_enemy_loc], (0,128,128), 0)
            g.pg.display.flip()
        if g.phase == Phase.Movement:
            input()
        if should_print: print("obs: ", obs)
        if should_print: print("reward: ", reward)
        if should_print: print("done: ", done)
    if game_num % 100 == 0:
        print(f"game {game_num} done")
    return num_turns, g.p1.damage, g.p2.damage, p1_rewards, p2_rewards

def main():
    human_playing = False
    # human_playing = True
    # does_draw = False
    does_draw = True
    # should_print = False
    should_print = True

    # dont_mp = True
    dont_mp = False

    num_games = 10000
    num_actual_games = 0
    all_num_turns = []
    p1_total_dmg = 1
    p2_total_dmg = 1
    p1_wins = 0
    p2_wins = 0

    # game_type = Game_Only_Move_Steps
    game_type = CaptainSonar

    if human_playing:
        actor1 = Human_Actor
        actor2 = Expert_Actor
    else:
        actor1 = Expert_Actor
        actor2 = Random_Actor

    if not does_draw and not should_print and not human_playing and not dont_mp:
        pool = mp.Pool(processes=mp.cpu_count())
        map_result = pool.map_async(run_one_game, [(does_draw, should_print, actor1, actor2, i, game_type) for i in range(num_games)])
        result_log = map_result.get()
        pool.close()
    else:
        pg = __import__("pygame")
        result_log = []
        for i in range(num_games):
            result_log.append(run_one_game((does_draw, should_print, actor1, actor2, i, game_type)))

    p1_rewards = []
    p2_rewards = []

    for num_turns, p1_dmg, p2_dmg, p1_rewards_one_game, p2_rewards_one_game in result_log:
        p1_rewards.append(sum(p1_rewards_one_game))
        p2_rewards.append(sum(p2_rewards_one_game))
        p1_total_dmg += p1_dmg
        p2_total_dmg += p2_dmg
        all_num_turns.append(num_turns)
        num_actual_games += 1
        if p2_dmg >= 4:
            p1_wins += 1
        elif p1_dmg >= 4:
            p2_wins += 1
        else:
            raise Exception("game ended with no winner")


    print("----------------------final stats-----------------------------")
    print("total games finished: ", num_actual_games)
    print("p1 total dmg: ", p1_total_dmg)
    print("p2 total dmg: ", p2_total_dmg)
    print("ratio: ", p1_total_dmg/p2_total_dmg)
    print("avg turns: ", sum(all_num_turns)/len(all_num_turns))
    print("p1 wins: ", p1_wins)
    print("p2 wins: ", p2_wins)
    print("p1 win ratio: ", p1_wins/num_actual_games)
    print("p2 win ratio: ", p2_wins/num_actual_games)
    print("p1 avg reward: ", sum(p1_rewards)/len(p1_rewards))
    print("p2 avg reward: ", sum(p2_rewards)/len(p2_rewards))
    if does_draw: pg.quit()

def test_only_moves_game():
    from .Captain_Sonar_Only_Move import Game
    game = Game()
    p1_rewards = []
    p2_rewards = []
    p1_actor = Random_Actor(game.env.ACTION_DICT, game.env.REVERSE_ACTION_DICT, game.env.board)
    game.reset()
    for _ in range(1000):
        game.reset()
        done = False
        while not done:
            if game.env.to_play() == 0:
                options = game.legal_actions()
                action = p1_actor.choose_action(options, game.env.observation)
                was_p1 = True
            else:
                was_p1 = False
                action = game.expert_agent()
            obs, reward, done = game.step(action)
            if was_p1:
                p1_rewards.append(reward)
            else:
                p2_rewards.append(reward)
    print("p1 rewards: ", sum(p1_rewards)/len(p1_rewards))
    print("p1 total rewards: ", sum(p1_rewards))
    print("len p1 rewards: ", len(p1_rewards))
    print("p2 rewards: ", sum(p2_rewards)/len(p2_rewards))
    print("p2 total rewards: ", sum(p2_rewards))
    print("len p2 rewards: ", len(p2_rewards))


if __name__ == "__main__":
    main()
    # test_only_moves_game()