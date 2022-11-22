from .game.game_only_move_steps import Game_Only_Move_Steps
from .Captain_Sonar import Game
from .muzero_config import MuZeroConfig
import datetime
import os
import pathlib

MuZeroConfig.results_path = pathlib.Path(os.path.join(os.path.dirname('/content/drive/My Drive'), "../results", os.path.basename(__file__)[:-3], datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")))  # Path to store the model weights and TensorBoard logs

class Game(Game):

    def __init__(self, seed=None):
        self.env = Game_Only_Move_Steps()