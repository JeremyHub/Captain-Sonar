from typing import Any


class Actor:

    def __init__(self, action_dict: dict, reverse_action_dict: dict, board: tuple):
        self.action_dict = action_dict
        self.reverse_action_dict = reverse_action_dict
        self.action_history = []
        self.obs_history = []
        self.unexamined_first_phase_obs = []
        self.last_phase_num = 2
        self.board = board

    def choose_action(self, actions: list, obs: list):
        # only add to first turn history if its the second obs in a row where the phase is choose power (or if its the first turn of the game)
        #    this works becuase there will always be a choose power at the start of your turn and at the end of your turn
        #       even if you choose a power at the end, there will be a choose power again until you dont choose a power to let you do multiple powers
        obs = obs[0][0]
        if self.last_phase_num == 2 and obs[4] == 2:
            self.unexamined_first_phase_obs.append(obs)
        self.last_phase_num = obs[4]

        self.obs_history.append(obs)
        action = self._choose_action(actions, obs)
        self.action_history.append(action)
        return action

    def _choose_action(actions, obs):
        raise NotImplementedError("subclasses need to implement _choose_action")
