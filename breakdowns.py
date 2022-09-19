from enum import Enum
from dataclasses import dataclass
from constants import Direction


class BreakdownChannel(Enum):
    Yellow = "yellow"
    Orange = "orange"
    Black = "black"
    Radiation = "radiation"
    No_Channel = "none"


class BreakdownType(Enum):
    Red = "red"
    Yellow = "yellow"
    Green = "green"
    Radiation = "radiation"


@dataclass
class BreakdownDot:
    channel: BreakdownChannel
    type: BreakdownType
    direction_class: Direction
    marked: bool = False

    def __repr__(self) -> str:
        return f"{self.type.value} dot on {self.channel.value} channel, at {self.direction_class.value} direction, is {self.marked} marked."


class BreakdownMap:
    def __init__(self):
        self.map = {}
        self.map[Direction.West] = [
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Red, Direction.West),
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Yellow, Direction.West),
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Green, Direction.West),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Green, Direction.West),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.West),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.West),
        ]
        self.map[Direction.North] = [
            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Yellow, Direction.North),
            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Yellow, Direction.North),
            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Red, Direction.North),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Green, Direction.North),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Red, Direction.North),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.North),
        ]
        self.map[Direction.South] = [
            BreakdownDot(BreakdownChannel.Black, BreakdownType.Green, Direction.West),
            BreakdownDot(BreakdownChannel.Black, BreakdownType.Yellow, Direction.West),
            BreakdownDot(BreakdownChannel.Black, BreakdownType.Red, Direction.West),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Red, Direction.West),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.West),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Yellow, Direction.West),
        ]
        self.map[Direction.East] = [
            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Green, Direction.East),
            BreakdownDot(BreakdownChannel.Black, BreakdownType.Yellow, Direction.East),
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Red, Direction.East),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.East),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Green, Direction.East),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.East),
        ]