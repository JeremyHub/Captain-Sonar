from enum import Enum


class Direction(Enum):
    North = "north"
    South = "south"
    West = "west"
    East = "east"


class Player(Enum):
    One = "player one"
    Two = "player two"


class Power(Enum):
    Mine = "mine"
    Drone = "drone"
    Silence = "silence"
    Torpedo = "torpedo"
    Sonar = "sonar"