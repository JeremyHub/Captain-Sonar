from enum import Enum
from dataclasses import dataclass
from constants import Direction, Power


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


POWER_TO_BREAKDOWN_TYPE = {
    Power.Drone: BreakdownType.Green,
    Power.Silence: BreakdownType.Yellow,
    Power.Torpedo: BreakdownType.Red,
}


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
        self.all_breakdowns = [
            # this list in order of appearence from left to right on the board (important for drawing)
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Red, Direction.West),
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Yellow, Direction.West),
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Green, Direction.West),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Green, Direction.West),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.West),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.West),

            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Yellow, Direction.North),
            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Red, Direction.North),
            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Yellow, Direction.North),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Green, Direction.North),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Red, Direction.North),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.North),

            BreakdownDot(BreakdownChannel.Black, BreakdownType.Green, Direction.South),
            BreakdownDot(BreakdownChannel.Black, BreakdownType.Yellow, Direction.South),
            BreakdownDot(BreakdownChannel.Black, BreakdownType.Red, Direction.South),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Red, Direction.South),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.South),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Yellow, Direction.South),

            BreakdownDot(BreakdownChannel.Orange, BreakdownType.Green, Direction.East),
            BreakdownDot(BreakdownChannel.Black, BreakdownType.Yellow, Direction.East),
            BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Red, Direction.East),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.East),
            BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Green, Direction.East),
            BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.East),
        ]

        self.direction_map = {}
        for breakdown in self.all_breakdowns:
            self.direction_map[breakdown.direction_class] = self.direction_map.get(breakdown.direction_class, [])
            self.direction_map[breakdown.direction_class].append(breakdown)

        self.channel_map = {}
        for breakdown in self.all_breakdowns:
            self.channel_map[breakdown.channel] = self.channel_map.get(breakdown.channel, [])
            self.channel_map[breakdown.channel].append(breakdown)

        self.type_map = {}
        for breakdown in self.all_breakdowns:
            self.type_map[breakdown.type] = self.type_map.get(breakdown.type, [])
            self.type_map[breakdown.type].append(breakdown)