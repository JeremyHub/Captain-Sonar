from dataclasses import dataclass

from game.breakdowns import BreakdownMap
from game.constants import Power


NUM_BREAKDOWNS = len(BreakdownMap().all_breakdowns)

@dataclass
class Public_Actions:
    """
    represent what you did in a turn,
    but only the stuff the opponent sees at the start of their turn
    """
    direction_moved: int = -1
    torpedo_used: int = 0
    torpedo_row: int = -1
    torpedo_col: int = -1
    silence_used: int = 0
    surface_quadrant: int = -1
    drone_used: int = 0

    def get_obs_arr(self):
        return list(self.__dict__.values())


@dataclass
class Observation:
    """
    observation of everything a player can see about the game
    -1 means n/a

    maybe to add:
    the map??
    """
    opp_actions: Public_Actions = None
    breakdowns: list = None
    power_marks: dict[Power, int] = None
    your_dmg: int = -1
    opp_dmg: int = -1
    row: int = -1
    col: int = -1
    phase_num: int = -1
    opp_quadrant: int = -1 # for drones power


    def get_obs_arr(self):
        assert self.opp_actions is not None
        assert len(self.breakdowns) == NUM_BREAKDOWNS
        assert len(self.power_marks) == len(Power)
        return [
            self.your_dmg,
            self.opp_dmg,
            self.row,
            self.col,
            self.phase_num,
            self.opp_quadrant
        ] + self.opp_actions.get_obs_arr() + self.breakdowns + self.power_marks
