from actors.expert_actor import Expert_Actor
from game.game import CaptainSonar
from game.observation import Observation
from game.observation import Public_Actions


class Game_Only_Move_Steps(CaptainSonar):
    def __init__(self, does_draw = False):
        super().__init__(does_draw)
        self.reset()

    def step(self, action):
        # observation = super()._update_observation(Observation(Public_Actions())).get_obs_arr()
        observation, reward1, done = super().step(action)
        while not observation[4] in [4,1] and not done:
            if self.to_play() == 1:
                reccomendation = self.a1.choose_action(self.legal_actions(), observation)
            else:
                reccomendation = self.a2.choose_action(self.legal_actions(), observation)
            observation, reward, done = super().step(reccomendation)
        return observation, reward1, done

    def reset(self):
        super().reset()
        self.a1 = Expert_Actor(self.ACTION_DICT, self.REVERSE_ACTION_DICT, self.board)
        self.a2 = Expert_Actor(self.ACTION_DICT, self.REVERSE_ACTION_DICT, self.board)
