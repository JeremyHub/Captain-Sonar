from random import randint
from typing import Any

from game.breakdowns import BreakdownChannel, BreakdownMap
from actors.actor import Actor


class Expert_Actor(Actor):
    
    def __init__(self, action_dict: dict[Any, int], reverse_action_dict: dict[int, Any]):
        super().__init__(action_dict, reverse_action_dict)
        self.breakdowns_on_paths = set()
        self.breakdowns = BreakdownMap()
        for breakdown in self.breakdowns.all_breakdowns:
            if breakdown.channel not in [BreakdownChannel.No_Channel, BreakdownChannel.Radiation]:
                self.breakdowns_on_paths.add(breakdown)


    def choose_action(self, actions: list[int], obs: list[int]):
        # if its aim power phase
        if obs[4] == 3 and len(actions) > 1:
            # if its torpedo
            if isinstance(self.reverse_action_dict[actions[1]][0], int):
                should_continue = False
                for index, action in enumerate(actions):
                    loc = self.reverse_action_dict[action]
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
            # TODO: build a model of where the enemy sub could be
            # use that model to get an average position of all the posiblities
            # use the std variation as a confidence
            # use that confidence as a weight for how much to weigh decideing to go in that direction
            # take that score in conjunction with the breakdowns to decide which direction to go

            # choose the direction with the least breakdowns
            num_marked = {}
            for i, action in enumerate(actions):
                direction = self.reverse_action_dict[action]
                for breakdown, marked in zip(self.breakdowns.all_breakdowns, obs[13:(13+len(self.breakdowns.all_breakdowns))]):
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
            if least_marked in [1,-1]:
                return 0
            return best_dir
        # if its the breadkown phase
        elif obs[4] == 5 and len(actions) > 1:
            # priotitize breakdowns that are part of channels so we can increase clearing
            for i, action in enumerate(actions):
                if self.reverse_action_dict[action] in self.breakdowns_on_paths:
                    return i
        # TODO: use the model of where the sub is to decide where to fire a torpedo
        # TODO: choose to fire a torpedo only when a possiblity is within range
        if len(actions) > 1 and obs and obs[4] in [4, 2]:
            action = randint(1,len(actions)-1)
        else:
            action = randint(0,len(actions)-1)
        return action