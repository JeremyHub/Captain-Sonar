from ..actors.expert_actor import Expert_Actor
from .game import CaptainSonar


class Game_Only_Move_Steps(CaptainSonar):
    def __init__(self, does_draw = False):
        super().__init__(does_draw)
        self.reset()

    def step(self, action):
        observation, reward1, done = super().step(action)
        while not observation[0][0][4] in [4,1] and not done:
            reccomendation = self.actor.choose_action(self.legal_actions(), observation)
            observation, reward, done = super().step(reccomendation)
        observation[0][0][4] = self.actor.average_enemy_loc[0]
        observation[0][0][5] = self.actor.average_enemy_loc[1]
        self.observation = observation
        return observation, reward1, done

    def reset(self):
        self.observation = super().reset()
        self.a1 = Expert_Actor(self.ACTION_DICT, self.REVERSE_ACTION_DICT, self.board)
        self.a2 = Expert_Actor(self.ACTION_DICT, self.REVERSE_ACTION_DICT, self.board)
        return self.observation

    @property
    def actor(self):
        if self.to_play() == 1:
            return self.a1
        else:
            return self.a2
