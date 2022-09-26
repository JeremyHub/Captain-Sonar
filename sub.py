from constants import DIRECTION_COORDS, Power, Direction, Player, POWER_COSTS, DIRECTION_COORDS
from breakdowns import BreakdownMap, BreakdownChannel, POWER_TO_BREAKDOWN_TYPE


class Sub:
    loc: tuple[int, int]
    path: list[tuple[int, int]]
    breakdownMap: BreakdownMap
    powers: dict[Power, int]
    player: Player
    remaining_surface_turns: int
    board: list[list[int]]


    def __init__(self, player: Player, board: list[list[int]]):
        self.player = player
        self.board = board
        self.loc = (-1,-1)
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
            self.loc = self._get_coord_in_direction(self.loc, direction)
        assert self.board[self.loc[0]][self.loc[1]] == 0, "trying to move to an island"

    
    def breakdown(self, dot, declared_direction):
        if declared_direction is None: # surfacing
            return
        for breakdown in self.breakdownMap.direction_map[declared_direction]:
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


    def silence(self, action):
        dir, speed = action
        for _ in range(speed):
            self.move(dir)

    
    def get_active_powers(self):
        active = [None]
        if self.remaining_surface_turns:
            return active
        for power, marks in self.powers.items():
            if power == Power.Silence:
                if len(self.get_valid_directions()) == 1:
                    # cant silence without anywhere to move to
                    continue
            cost = POWER_COSTS[power]
            assert marks <= cost and marks >= 0, "{} on {} power".format(marks, power)
            if marks == cost:
                for breakdown in self.breakdownMap.type_map[POWER_TO_BREAKDOWN_TYPE[power]]:
                    if breakdown.marked:
                        break
                else: # if above for loop does not break
                    active.append(power)
        return active


    def get_unbroken_breakdowns(self, direction):
        if direction is None: # surfacing
            return [None]
        options = []
        for breakdown in self.breakdownMap.direction_map[direction]:
            if not breakdown.marked:
                options.append(breakdown)
        assert options, "all breakdowns are marked"
        return options


    def get_valid_directions(self):
        valid_directions = [None]
        if self.remaining_surface_turns:
            return valid_directions
        for direction in Direction:
            row,col = self._get_coord_in_direction(self.loc, direction)
            if self._in_bounds(row, col):
                if self.board[row][col] == 0 and (row,col) not in self.path:
                    valid_directions.append(direction)
        return valid_directions

    
    def get_unmarked_powers(self):
        if self.remaining_surface_turns:
            return [None]
        powers = [p for p in Power if POWER_COSTS[p] > self.powers[p]]
        return powers if powers else [None]


    def get_power_options(self, power):
        options = []
        if power == Power.Silence:
            options = self._get_silence_options()
        elif power == Power.Torpedo:
            options = self._get_torpedo_options()
        else:
            raise Exception("power not found")
        assert options, "no options for aiming power"
        return options


    def get_quadrant(self):
        col_half = int(self.loc[1] > len(self.board[0])-1)
        row_half = int(self.loc[0] > len(self.board)-1)
        return col_half + 2*row_half


    def _get_silence_options(self):
        options = []
        for dir in Direction:
            loc = self.loc
            for i in range(4):
                row_dir, col_dir = self._get_coord_in_direction(loc, dir)
                if self._in_bounds(row_dir, col_dir) and self.board[row_dir][col_dir] == 0 and (row_dir, col_dir) not in self.path:
                    options.append((dir, i))
                    loc = (row_dir, col_dir)
                else:
                    break
        return options


    def _in_bounds(self, row, col):
        return 0 <= row < len(self.board) and 0 <= col < len(self.board[0])


    def _get_torpedo_options(self):
        options = []
        to_check = [self.loc]
        for _ in range(4):
            to_add = []
            for option in to_check:
                for dir in Direction:
                    loc = self._get_coord_in_direction(option, dir)
                    if loc in options:
                        continue
                    if self._in_bounds(loc[0], loc[1]) and self.board[loc[0]][loc[1]] == 0:
                        options.append(loc)
                        to_add.append(loc)
            to_check = to_add
        return options

    
    def _get_coord_in_direction(self, loc, direction):
        dir_col, dir_row = DIRECTION_COORDS[direction]
        row = loc[0] + dir_row
        col = loc[1] + dir_col
        return (row,col)


    def _check_breakdown_clearing(self):
        # check for damage if all on one direction are broken
        # or damage for radiation
        # or clearing all on one channel
        for breakdown_map in [self.breakdownMap.direction_map.items(), self.breakdownMap.channel_map.items()]:
            for channel_or_direction, breakdowns in breakdown_map:
                for breakdown in breakdowns:
                    if not breakdown.marked:
                        break
                else: # if above loop does not break
                    for breakdown in breakdowns:
                        breakdown.marked = False
                    if type(channel_or_direction) == Direction:
                        self.damage += 1
                    if channel_or_direction == BreakdownChannel.Radiation:
                        self.damage += 1

    
    def _surface(self):
        assert self.remaining_surface_turns == 0, "trying to surface while already surfaced"
        self.path = []
        self.breakdownMap = BreakdownMap()
        self.remaining_surface_turns = 3