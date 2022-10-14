from random import randint

from game.breakdowns import BreakdownChannel, BreakdownMap


breakdowns_on_paths = set()
breakdowns = BreakdownMap()
for breakdown in breakdowns.all_breakdowns:
    if breakdown.channel not in [BreakdownChannel.No_Channel, BreakdownChannel.Radiation]:
        breakdowns_on_paths.add(breakdown)

def choose_action(actions, obs, action_dict, reverse_action_dict):

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
    elif obs[4] == 4 and len(actions) > 1:
        # choose the direction with the least breakdowns
        num_marked = {}
        for i, action in enumerate(actions):
            direction = reverse_action_dict[action]
            for breakdown, marked in zip(breakdowns.all_breakdowns, obs[13:(13+len(breakdowns.all_breakdowns))]):
                if not marked:
                    if breakdown.direction_class == direction:
                        num_marked[i] = num_marked.get(i, 0) + 1
        least_marked = -1
        best_dir = None
        for key, val in num_marked.items():
            if val > least_marked:
                least_marked = val
                best_dir = key
        # if we will take damage, surface instead
        if least_marked == 1:
            return 0
        return best_dir
    # if its the breadkown phase
    elif obs[4] == 5 and len(actions) > 1:
        # priotitize breakdowns that are part of channels so we can increase clearing
        for i, action in enumerate(actions):
            if reverse_action_dict[action] in breakdowns_on_paths:
                return i
    if len(actions) > 1 and obs and obs[4] in [4, 2]:
        action = randint(1,len(actions)-1)
    else:
        action = randint(0,len(actions)-1)
    return action