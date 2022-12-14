from random import randint
from typing import Any

from .actor import Actor

class Random_Actor(Actor):
    
    def __init__(self, action_dict: dict[Any, int], reverse_action_dict: dict[int, Any], board: tuple[tuple[int]]):
        super().__init__(action_dict, reverse_action_dict, board)


    def _choose_action(self, actions: list[int], obs: list[int]):
        # if phase is mov or choose power, dont do nothing
        if len(actions) > 1 and obs[4] in [2]:
            action = randint(1,len(actions)-1)
        else:
            action = randint(0,len(actions)-1)
        return actions[action]