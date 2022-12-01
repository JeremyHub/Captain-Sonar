from actors.expert_actor import Expert_Actor
from .game.game_only_move_steps import Game_Only_Move_Steps
from .Captain_Sonar import Game
from .muzero_config import MuZeroConfig

class Game(Game):

    def __init__(self, seed=None):
        self.env = Game_Only_Move_Steps()


    def expert_agent(self):
        if self.expert == None:
            self.expert = Expert_Actor(self.env.ACTION_DICT, self.env.REVERSE_ACTION_DICT, self.env.board)
        self.expert.possible_opp_positions = [(self.env.observation[0][0][4], self.env.observation[0][0][5])]
        return self.expert._choose_action(self.legal_actions(), self.env.observation, should_update=False)
