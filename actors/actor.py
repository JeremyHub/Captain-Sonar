from typing import Any


class Actor:

    def __init__(self, action_dict: dict[Any, int], reverse_action_dict: dict[int, Any]):
        self.action_dict = action_dict
        self.reverse_action_dict = reverse_action_dict

    def choose_action(self, actions: list[int], obs: list[int]):
        pass
