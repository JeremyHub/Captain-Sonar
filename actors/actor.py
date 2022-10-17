from typing import Any


class Actor:

    def __init__(self, action_dict: dict[Any, int], reverse_action_dict: dict[int, Any]):
        self.action_dict = action_dict
        self.reverse_action_dict = reverse_action_dict
        self.action_history = []
        self.obs_history = []

    def choose_action(self, actions: list[int], obs: list[int]):
        self.obs_history.append(obs)
        action = self._choose_action(actions, obs)
        self.action_history.append(action)
        return action
