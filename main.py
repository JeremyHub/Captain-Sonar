from game.game import Game, Phase
import pygame as pg
from game.observation import Observation, Public_Actions
from actors.random_actor import Random_Actor
from actors.expert_actor import Expert_Actor

if __name__ == "__main__":
    does_draw = False
    # does_draw = True
    should_print = False
    # should_print = True
    g = Game(does_draw)
    num_games = 0
    num_turns = 0
    all_num_turns = []
    p1_total_dmg = 1
    p2_total_dmg = 1
    done = True
    try:
        while True:
            if done:
                obs = g._update_observation(Observation(Public_Actions())).get_obs_arr()
                # TODO: everything breaks if there are two expert actors
                p1 = Random_Actor(g.ACTION_DICT, g.REVERSE_ACTION_DICT, g.board)
                p2 = Expert_Actor(g.ACTION_DICT, g.REVERSE_ACTION_DICT, g.board)
                p1_total_dmg += g.p1.damage
                p2_total_dmg += g.p2.damage
                g = Game(does_draw)
                num_games += 1
                all_num_turns.append(num_turns)
                num_turns = 0
                if not num_games % 100:
                    print(num_games)
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
    finally:
        print("----------------------final stats-----------------------------")
        print(num_games)
        print("p1 total dmg: ", p1_total_dmg)
        print("p2 total dmg: ", p2_total_dmg)
        print("ratio: ", p1_total_dmg/p2_total_dmg)
        print("avg turns: ", sum(all_num_turns)/len(all_num_turns))
        pg.quit()
