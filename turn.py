from dataclasses import dataclass
from constants import Player, Power, Direction

@dataclass
class Turn:
    player: Player
    direction: Direction
    powers_used: list[tuple[Power, any]]
    damage: int