from enum import Enum


class Direction(Enum):
    North = "north"
    South = "south"
    West = "west"
    East = "east"

DIRECTION_COORDS = { #col, row
    Direction.North: (0,-1),
    Direction.South: (0,1),
    Direction.West: (-1,0),
    Direction.East: (1,0)
}

class Power(Enum):
    Drone = "drone"
    Silence = "silence"
    Torpedo = "torpedo"

class Player(Enum):
    One = "player one"
    Two = "player two"

POWER_COSTS = {
    Power.Torpedo: 3,
    Power.Drone: 4,
    Power.Silence: 6
}

ALPHA_BOARD = (
    #A B C D E F G H I J K L M N O
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), # 1
    (0,0,1,0,0,0,1,0,0,0,0,0,1,1,0), # 2
    (0,0,1,0,0,0,0,0,1,0,0,0,1,0,0), # 3
    (0,0,0,0,0,0,0,0,1,0,0,0,0,0,0), # 4
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), # 5
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), # 6
    (0,1,0,1,0,0,1,0,1,0,0,0,0,0,0), # 7
    (0,1,0,1,0,0,1,0,0,0,0,0,0,0,0), # 8
    (0,0,0,1,0,0,0,1,0,0,0,1,1,1,0), # 9
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), # 10
    (0,0,0,1,0,0,0,0,0,0,0,0,0,0,0), # 11
    (0,0,1,0,0,0,0,1,0,0,0,1,0,0,0), # 12
    (1,0,0,0,0,0,0,0,0,0,0,0,1,0,0), # 13
    (0,0,1,0,0,0,1,0,1,0,0,0,0,1,0), # 14
    (0,0,0,1,0,0,0,0,0,0,0,0,0,0,0), # 15
)

SCREEN_LOCS = {
    Power: {
        Power.Silence: lambda size: size*2,
        Power.Drone: lambda size: size*2,
        Power.Torpedo: lambda size: size*2,
    }
}