from constants import DIRECTION_COORDS, Power, Direction, Player, POWER_COSTS, DIRECTION_COORDS
from breakdowns import BreakdownMap, BreakdownChannel, BreakdownType


class Sub:
    loc: tuple[int, int]
    path: list[tuple[int, int]]
    breakdownMap: BreakdownMap
    powers: dict[Power, int]
    player: Player
    remaining_surface_turns: int


    def __init__(self, player: Player):
        self.player = player
        self.loc = None
        self.path = []
        self.breakdownMap = BreakdownMap()
        self.powers = {k:0 for k in Power}
        self.damage = 0
        self.remaining_surface_turns = 0

    
    def set_starting_loc(self, loc: tuple[int, int]):
        assert self.path == [], "setting starting loc of existing sub"
        self.loc = loc

    
    def move(self, direction):
        if direction is None and not self.remaining_surface_turns:
            self._surface()
        elif direction is None and self.remaining_surface_turns:
            self.remaining_surface_turns -= 1
        else:
            self.path.append(self.loc)
            self.loc = self._get_coord_in_direction(direction)

    
    def breakdown(self, dot, declared_direction):
        if declared_direction is None: # surfacing
            return
        for breakdown in self.breakdownMap.map[declared_direction]:
            if breakdown == dot:
                assert not breakdown.marked, "trying to disable already marked breakdown"
                breakdown.marked = True
                break
        else: # if above for loop doesnt break
            raise Exception("breakdown not found")
        self._check_breakdown_clearing()
    

    def mark(self, power):
        if power is not None:
            self.powers[power] += 1

    
    def get_active_powers(self):
        active = [None]
        if self.remaining_surface_turns:
            active
        for power, marks in self.powers.items():
            cost = POWER_COSTS[power]
            assert marks <= cost and marks >= 0, "{} on {} power".format(marks, power)
            if marks == cost:
                active.append(power)
        return active


    def get_unbroken_breakdowns(self, direction):
        if direction is None: # surfacing
            return [None]
        options = []
        for breakdown in self.breakdownMap.map[direction]:
            if not breakdown.marked:
                options.append(breakdown)
        assert options, "all breakdowns are marked"
        return options


    def get_valid_directions(self, board):
        valid_directions = [None]
        if self.remaining_surface_turns:
            return valid_directions
        for direction in Direction:
            row,col = self._get_coord_in_direction(direction)
            if 0 < row < len(board) and 0 < col < len(board[0]):
                if board[row][col] == 0 and (row,col) not in self.path:
                    valid_directions.append(direction)
        return valid_directions

    
    def get_unmarked_powers(self):
        if self.remaining_surface_turns:
            return [None]
        powers = [p for p in Power if p not in self.get_active_powers()]
        return powers if powers else [None]


    def get_quadrant(self, board):
        col_half = int(self.loc[1] > len(board[0])-1)
        row_half = int(self.loc[0] > len(board)-1)
        return col_half + 2*row_half

    
    def _get_coord_in_direction(self, direction):
        dir_col, dir_row = DIRECTION_COORDS[direction]
        row = self.loc[0] + dir_row
        col = self.loc[1] + dir_col
        return (row,col)


    def _check_breakdown_clearing(self):
        # check for damage if all on one direction are broken
        for breakdowns in self.breakdownMap.map.values():
            for breakdown in breakdowns:
                if not breakdown.marked:
                    break
            else: # if above loop does not break
                for breakdown in breakdowns:
                    breakdown.marked = False
                    self.damage += 1
        # check for the channels and radiation
        any_unmarked_in_channels = {
            BreakdownChannel.Yellow: False,
            BreakdownChannel.Orange: False,
            BreakdownChannel.Black: False,
            BreakdownChannel.Radiation: False,
        }
        for breakdown in [b for bl in self.breakdownMap.map.values() for b in bl]:
            if not breakdown.marked:
                any_unmarked_in_channels[breakdown.channel] = True
        for channel, any_unmarked in any_unmarked_in_channels.items():
            if not any_unmarked:
                if channel == BreakdownChannel.Radiation:
                    self.damage += 1
                for breakdown in [b for bl in self.breakdownMap.map.values() for b in bl]:
                    if breakdown.channel == channel:
                        assert breakdown.marked, "channel was all marked, but one of the dots is not"
                        breakdown.marked = False

    
    def _surface(self):
        assert self.remaining_surface_turns == 0, "trying to surface while already surfaced"
        self.path = []
        self.breakdownMap = BreakdownMap()
        self.remaining_surface_turns = 3