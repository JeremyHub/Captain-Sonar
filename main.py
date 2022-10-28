from game.game import CaptainSonar, Phase
from game.observation import Observation, Public_Actions
from actors.random_actor import Random_Actor
from actors.expert_actor import Expert_Actor
import multiprocessing as mp


def run_one_game(tuple_of_args):
    does_draw, should_print, actor1, actor2, game_num = tuple_of_args
    g = CaptainSonar(does_draw)
    obs = g._update_observation(Observation(Public_Actions())).get_obs_arr()
    # TODO: everything breaks if the expert is the first one
    p1 = actor1(g.ACTION_DICT, g.REVERSE_ACTION_DICT, g.board)
    p2 = actor2(g.ACTION_DICT, g.REVERSE_ACTION_DICT, g.board)
    done = False
    num_turns = 0
    while not done:
        if should_print: print("---------------------------------------")
        if should_print: print("player: ", g.player.player)
        options = g.legal_actions()
        if g.to_play() == 1:
            action = p1.choose_action(options, obs)
        elif g.to_play() == 2:
            action = p2.choose_action(options, obs)
        if should_print: print("phase: ", g.phase)
        if should_print: print("options: ", options)
        if should_print: print("action: ", g.REVERSE_ACTION_DICT[action])
        obs, reward, done = g.step(action)
        if g.phase == Phase.Movement:
            num_turns += 1
        if does_draw:
            g.pg_draw_points(p2.possible_opp_positions, (255,255,255), 10)
            g.pg_draw_points([p2.average_enemy_loc], (0,128,128), 0)
            pg.display.flip()
            # if g.phase == Phase.Movement:
            #     input()
        if should_print: print("obs: ", obs)
        if should_print: print("reward: ", reward)
        if should_print: print("done: ", done)
    if game_num % 100 == 0:
        print(f"game {game_num} done")
    return num_turns, g.p1.damage, g.p2.damage

if __name__ == "__main__":
    does_draw = False
    # does_draw = True
    should_print = False
    # should_print = True

    num_games = 30000
    num_actual_games = 0
    all_num_turns = []
    p1_total_dmg = 1
    p2_total_dmg = 1
    p1_wins = 0
    p2_wins = 0
    
    if not does_draw:
        pool = mp.Pool(processes=mp.cpu_count())
        map_result = pool.map_async(run_one_game, [(does_draw, should_print, Random_Actor, Expert_Actor, i) for i in range(num_games)])
        result_log = map_result.get()
        pool.close()
    else:
        pg = __import__("pygame")
        result_log = []
        for _ in range(num_games):
            result_log.append(run_one_game((does_draw, should_print, Random_Actor, Expert_Actor, 0)))

    for num_turns, p1_dmg, p2_dmg in result_log:
        p1_total_dmg += p1_dmg
        p2_total_dmg += p2_dmg
        all_num_turns.append(num_turns)
        num_actual_games += 1
        if p2_dmg == 4:
            p1_wins += 1
        elif p1_dmg == 4:
            p2_wins += 1
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
    if does_draw: pg.quit()
