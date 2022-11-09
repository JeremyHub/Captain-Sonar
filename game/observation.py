from dataclasses import dataclass

from .breakdowns import BreakdownMap
from .constants import Power


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
    power_marks: dict = None
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


    def make_obs_from_arr(self, arr):
        # assert len(arr) == 12 + NUM_BREAKDOWNS + len(Power)
        self.your_dmg = arr[0]
        self.opp_dmg = arr[1]
        self.row = arr[2]
        self.col = arr[3]
        self.phase_num = arr[4]
        self.opp_quadrant = arr[5]
        self.opp_actions = Public_Actions()
        self.opp_actions.direction_moved = arr[6]
        self.opp_actions.torpedo_used = arr[7]
        self.opp_actions.torpedo_row = arr[8]
        self.opp_actions.torpedo_col = arr[9]
        self.opp_actions.silence_used = arr[10]
        self.opp_actions.surface_quadrant = arr[11]
        self.opp_actions.drone_used = arr[12]
        self.breakdowns = arr[13:13+NUM_BREAKDOWNS]
        self.power_marks = arr[13+NUM_BREAKDOWNS:]
