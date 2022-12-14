from enum import Enum
from dataclasses import dataclass
from .constants import Direction, Power


class BreakdownChannel(Enum):
    Yellow = 1
    Orange = 2
    Black = 3
    Radiation = 4
    No_Channel = 5


class BreakdownType(Enum):
    Red = 1
    Yellow = 2
    Green = 3
    Radiation = 4


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
        return str(self.channel.value) + str(self.direction_class.value) + str(self.type.value) + str(int(self.marked))


    def __hash__(self) -> int:
        return hash((self.channel, self.type, self.direction_class))


class BreakdownMap:
    def __init__(self):
        self.all_breakdowns = [
            # this list in order of appearence from left to right on the board in terms of directions (important for drawing)
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