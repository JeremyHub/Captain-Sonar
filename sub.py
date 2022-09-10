from constants import Power, Direction
from breakdowns import BreakdownMap

class Sub:
    loc: tuple[int, int]
    path: list[tuple[int, int]]
    breakdowns = BreakdownMap
    powers = dict[Power, int]

    def __init__(self, *, loc: tuple[int, int], path: list[tuple[int, int]], breakdowns: BreakdownMap, powers: dict[Power, int]):
        self.loc = loc if loc else None
        self.path = path if path else []
        self.breakdowns = breakdowns if breakdowns else BreakdownMap()
        self.powers = powers if powers else {k:0 for k in Power}