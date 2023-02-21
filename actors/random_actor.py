from random import randint
from typing import Any

from ..game.breakdowns import BreakdownChannel

from .actor import Actor

class Random_Actor(Actor):
    
    def __init__(self, action_dict: dict[Any, int], reverse_action_dict: dict[int, Any], board: tuple[tuple[int]]):
        super().__init__(action_dict, reverse_action_dict, board)


    def _choose_action(self, actions: list[int], obs: list[int]):
        # if phase is mov or choose power, dont do nothing
        if len(actions) > 1 and obs[4] in [2]:
            action = randint(1,len(actions)-1)
        elif obs[4] == 5 and len(actions) > 1:
            good_breakdowns = []
            for i, action in enumerate(actions):
                if not self.reverse_action_dict[action].channel == BreakdownChannel.No_Channel:
                    good_breakdowns.append(i)
            if good_breakdowns:
                action = randint(0,len(good_breakdowns)-1)
                action = good_breakdowns[action]
            else:
                action = randint(0,len(actions)-1)
        else:
            action = randint(0,len(actions)-1)
        return actions[action]