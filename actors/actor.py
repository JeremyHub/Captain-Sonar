from typing import Any


class Actor:

    def __init__(self, action_dict: dict[Any, int], reverse_action_dict: dict[int, Any], board: tuple[tuple[int]]):
        self.action_dict = action_dict
        self.reverse_action_dict = reverse_action_dict
        self.action_history = []
        self.obs_history = []
        self.first_phase_obs_history = []
        self.last_phase_num = 2
        self.board = board

    def choose_action(self, actions: list[int], obs: list[int]):
        # only add to first turn history if its the second obs in a row where the phase is choose power (or if its the first turn of the game)
        #    this works becuase there will always be a choose power at the start of your turn and at the end of your turn
        #       even if you choose a power at the end, there will be a choose power again until you dont choose a power to let you do multiple powers
        if self.last_phase_num == 2 and obs[4] == 2:
            self.first_phase_obs_history.append(obs)
        self.last_phase_num = obs[4]

        self.obs_history.append(obs)
        action = self._choose_action(actions, obs)
        self.action_history.append(action)
        return action
