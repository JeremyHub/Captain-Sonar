from enum import Enum
from dataclasses import dataclass
from constants import Direction


class BreakdownChannel(Enum):
    Yellow = "yellow"
    Orange = "orange"
    Black = "black"


class BreakdownType(Enum):
    Red = "red"
    Yellow = "yellow"
    Green = "green"
    Radiation = "radiation"


@dataclass
class BreakdownDot:
    channel: BreakdownChannel
    type: BreakdownType
    disabled: bool = False


class BreakdownMap:
    def __init__(self):
        self.map = {}
        self.map[Direction.West] = [
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Red),
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Yellow),
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Green),
            BreakdownDot(None, BreakdownType.Green),
            BreakdownDot(None, BreakdownType.Radiation),
            BreakdownDot(None, BreakdownType.Radiation),
        ]
        self.map[Direction.North] = [
            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Yellow),
            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Yellow),
            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Red),
            BreakdownDot(None, BreakdownType.Green),
            BreakdownDot(None, BreakdownType.Red),
            BreakdownDot(None, BreakdownType.Radiation),
        ]
        self.map[Direction.South] = [
            BreakdownDot(BreakdownChannel.Black, BreakdownType.Green),
            BreakdownDot(BreakdownChannel.Black, BreakdownType.Yellow),
            BreakdownDot(BreakdownChannel.Black, BreakdownType.Red),
            BreakdownDot(None, BreakdownType.Red),
            BreakdownDot(None, BreakdownType.Radiation),
            BreakdownDot(None, BreakdownType.Yellow),
        ]
        self.map[Direction.East] = [
            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Green),
            BreakdownDot(BreakdownChannel.Black, BreakdownType.Yellow),
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Red),
            BreakdownDot(None, BreakdownType.Radiation),
            BreakdownDot(None, BreakdownType.Green),
            BreakdownDot(None, BreakdownType.Radiation),
        ]