from typing import Any

from actors.actor import Actor
from actors.expert_actor import Expert_Actor
from game.observation import Observation

class Human_Actor(Actor):
    
    def __init__(self, action_dict: dict[Any, int], reverse_action_dict: dict[int, Any], board: tuple[tuple[int]]):
        super().__init__(action_dict, reverse_action_dict, board)
        self.expert_actor = Expert_Actor(action_dict, reverse_action_dict, board)


    def _choose_action(self, actions: list[int], obs_arr: list[int]):
        obs = Observation()
        obs.make_obs_from_arr(obs_arr)
        # print obs array with names of variables
        print("obs array:")
        print(obs.__dict__)
        # print actions with names in rev action dict
        print("actions:")
        reccomened_action = self.expert_actor.choose_action(actions, obs_arr)
        print("Reccomended action: " + str(self.reverse_action_dict[reccomened_action]))
        # if its mov phase
        if obs_arr[4] == 4 and len(actions) > 1:
            for i, action in enumerate(actions):
                print(i, self.reverse_action_dict[action])
        # ask for which action to take
            action = int(input("which action? "))
            return actions[action]
        else:
            return reccomened_action
