from constants import DIRECTION_COORDS, Power, Direction, Player, POWER_COSTS, DIRECTION_COORDS
from breakdowns import BreakdownMap


class Sub:
    loc: tuple[int, int]
    path: list[tuple[int, int]]
    breakdownMap: BreakdownMap
    powers: dict[Power, int]
    player: Player


    def __init__(self, player: Player,
        *,
        loc: tuple[int, int] = None,
        path: list[tuple[int, int]] = None,
        breakdownMap: BreakdownMap = None,
        powers: dict[Power, int] = None
    ):
        self.player = player
        self.loc = loc if loc else None
        self.path = path if path else []
        self.breakdownMap = breakdownMap if breakdownMap else BreakdownMap()
        self.powers = powers if powers else {k:0 for k in Power}

    
    def set_starting_loc(self, loc: tuple[int, int]):
        assert self.path == [], "setting starting loc of existing sub"
        self.loc = loc

    
    def move(self, direction):
        self.loc = self._get_coord_in_direction(direction)

    
    def breakdown(self, dot, declared_direction):
        for breakdown in self.breakdownMap.map[declared_direction]:
            if breakdown == dot:
                assert not breakdown.disabled, "trying to disable already disabled breakdown"
                breakdown.disabled = True
                return
        raise Exception("breakdown not found")

    
    def get_active_powers(self):
        active = []
        for power, marks in self.powers.items():
            cost = POWER_COSTS[power]
            assert marks <= cost and marks >= 0, "{} on {} power".format(marks, power)
            if marks == cost:
                active.append(power)
        return active


    def get_unbroken_breakdowns(self, direction):
        options = []
        for breakdown in self.breakdownMap.map[direction]:
            if not breakdown.disabled:
                options.append(breakdown)
        return options


    def get_valid_directions(self, board):
        valid_directions = []
        for direction in Direction:
            x,y = self._get_coord_in_direction(direction)
            if 0 < y < len(board) or 0 < x < len(board[0]):
                if board[x][y] == 0 and (x,y) not in self.path:
                    valid_directions.append(direction)
        return valid_directions

    
    def _get_coord_in_direction(self, direction):
        dirX, dirY = DIRECTION_COORDS[direction]
        x = self.loc[0] + dirX
        y = self.loc[1] + dirY
        return (x,y)
