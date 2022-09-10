from dataclasses import dataclass
from typing import Optional
from constants import Player, Power, Direction

@dataclass
class Turn:
    player: Player
    direction: Direction
    powers: list[Optional[tuple[Power, any]]]
    damage: int