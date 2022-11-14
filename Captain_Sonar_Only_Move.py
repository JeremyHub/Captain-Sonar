from .game.game_only_move_steps import Game_Only_Move_Steps
from .Captain_Sonar import Game

class Game(Game):

    def __init__(self, seed=None):
        self.env = Game_Only_Move_Steps()