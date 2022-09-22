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
        yredw = BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Red, Direction.West)
        yyw = BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Yellow, Direction.West)
        ygw = BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Green, Direction.West)
        ngw = BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Green, Direction.West)
        rrw1 = BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.West)
        rrw2 = BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.West)
        oyn1 = BreakdownDot(BreakdownChannel.Orange, BreakdownType.Yellow, Direction.North)
        oyn2 = BreakdownDot(BreakdownChannel.Orange, BreakdownType.Yellow, Direction.North)
        oredn = BreakdownDot(BreakdownChannel.Orange, BreakdownType.Red, Direction.North)
        ngn = BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Green, Direction.North)
        nredn = BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Red, Direction.North)
        rrn = BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.North)
        bgs = BreakdownDot(BreakdownChannel.Black, BreakdownType.Green, Direction.South)
        bys = BreakdownDot(BreakdownChannel.Black, BreakdownType.Yellow, Direction.South)
        breds = BreakdownDot(BreakdownChannel.Black, BreakdownType.Red, Direction.South)
        nreds = BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Red, Direction.South)
        rrs = BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.South)
        nys = BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Yellow, Direction.South)
        oge = BreakdownDot(BreakdownChannel.Orange, BreakdownType.Green, Direction.East)
        bye = BreakdownDot(BreakdownChannel.Black, BreakdownType.Yellow, Direction.East)
        yrede = BreakdownDot(BreakdownChannel.Yellow, BreakdownType.Red, Direction.East)
        rre1 = BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.East)
        nge = BreakdownDot(BreakdownChannel.No_Channel, BreakdownType.Green, Direction.East)
        rre2 = BreakdownDot(BreakdownChannel.Radiation, BreakdownType.Radiation, Direction.East)

        self.all_breakdowns = [yredw,yyw,ygw,ngw,rrw1,rrw2,oyn1,oyn2,oredn,ngn,nredn,rrn,bgs,bys,breds,nreds,rrs,nys,oge,bye,yrede,rre1,nge,rre2]

        self.direction_map = {}
        self.direction_map[Direction.West] = [yredw,yyw,ygw,ngw,rrw1,rrw2]
        self.direction_map[Direction.North] = [oyn1,oyn2,oredn,ngn,nredn,rrn]
        self.direction_map[Direction.South] = [bgs,bys,breds,nreds,rrs,nys]
        self.direction_map[Direction.East] = [oge,bye,yrede,rre1,nge,rre2]

        self.channel_map = {}
        self.channel_map[BreakdownChannel.Black] = [bgs, bys, breds, bye]
        self.channel_map[BreakdownChannel.No_Channel] = [ngw, ngn, nreds, nys, nge]
        self.channel_map[BreakdownChannel.Radiation] = [rrw1, rrw2, rrn, rrs, rre1, rre2]
        self.channel_map[BreakdownChannel.Orange] = [oyn1, oyn2, oredn, oge]
        self.channel_map[BreakdownChannel.Yellow] = [yredw, yyw, ygw, yrede]

        self.type_map = {}
        self.type_map[BreakdownType.Green] = [ygw, ngw, ngn, bgs, oge, nge]
        self.type_map[BreakdownType.Radiation] = [rrw1, rrw2, rrn, rrs, rre1, rre2]
        self.type_map[BreakdownType.Red] = [yredw, oredn, nreds, yrede]
        self.type_map[BreakdownType.Yellow] = [yyw, oyn1, oyn2, bys, nys, bye]