from random import randint

from game.breakdowns import BreakdownMap

def choose_action(actions, obs, action_dict, reverse_action_dict):
    # obs[4] is the phase

    # if its aim power phase
    if obs[4] == 3 and len(actions) > 1:
        # if its torpedo
        if isinstance(reverse_action_dict[actions[1]][0], int):
            should_continue = False
            for index, action in enumerate(actions):
                loc = reverse_action_dict[action]
                should_continue = False
                for i in range(-1,2):
                    for j in range(-1,2):
                        if loc[0]+i == obs[2] and loc[1]+j == obs[3]: should_continue = True
                        if should_continue: continue
                    if should_continue: continue
                if should_continue: continue
                return index
    # if its mov phase
    # elif obs[4] == 4 and len(actions) > 1:
        # choose the direction with the least breakdowns
    # if its the breadkown phase
    # elif obs[4] == 5 and len(actions) > 1:
        # prioritize breakdowns on paths, and specifically on paths that are already marked
        # breakdowns = BreakdownMap().direction_map[]
        # for breakdown, marked in zip(breakdowns, obs[13:(14+len(breakdowns))]):
        #     assert marked in (0,1)
        #     if breakdown.channel is not None and not marked:
    if len(actions) > 1 and obs and obs[4] in [4, 2]:
        action = randint(1,len(actions)-1)
    else:
        action = randint(0,len(actions)-1)
    return action