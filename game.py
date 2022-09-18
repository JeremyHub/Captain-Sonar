from enum import Enum
from turn import Turn
from sub import Sub
from constants import Player, Direction, ALPHA_BOARD


class Phase(Enum):
    Starting = "starting phase"
    Power = "power phase"
    Movement = "movement phase"
    Breakdown = "breakdown phase"


class Game:

    PHASES = [Phase.Power, Phase.Movement, Phase.Breakdown, Phase.Power]
    history: list[Turn]
    p1: Sub
    p2: Sub
    player: Sub
    phase: int or Phase
    board: tuple[tuple[int]]
    declared_direction: Direction
    

    def __init__(self):
        self.reset()


    def reset(self):
        self.history = []
        self.p1 = Sub(Player.One)
        self.p2 = Sub(Player.Two)
        self.player = self.p1
        self.phase = Phase.Starting
        self.board = ALPHA_BOARD
        self.declared_direction = None

    
    def step(self, action):
        if self.PHASES[self.phase] == Phase.Starting:
            self.player.set_starting_loc(action)
        elif self.PHASES[self.phase] == Phase.Power:
            pass
        elif self.PHASES[self.phase] == Phase.Movement:
            self.player.move(action)
            self.declared_direction = action
        elif self.PHASES[self.phase] == Phase.Breakdown:
            self.player.breakdown(action, self.declared_direction)
        self.next_phase()

    
    def legal_actions(self):
        if self.PHASES[self.phase] == Phase.Starting:
            actions = []
            for x in range(self.board):
                for y in range(self.board[x]):
                    if self.board[x][y] == 0:
                        actions.append((x,y))
            return actions
        elif self.PHASES[self.phase] == Phase.Power:
            return self.player.get_active_powers()
        elif self.PHASES[self.phase] == Phase.Movement:
            return self.player.get_valid_directions()
        elif self.PHASES[self.phase] == Phase.Breakdown:
            return self.player.get_unbroken_breakdowns(self.declared_direction)
        raise Exception("phase is not a valid phase")


    def next_phase(self):
        """
        Changes the current phase to the next one.
        Also changes current player to other one if its the end of the last phase.
        """
        if self.phase == Phase.Starting:
            if self.player == self.p1:
                self.player = self.p2
            else:
                assert self.player == self.p2, "player is not p1 or p2 in starting phase"
                self.phase = 0
                self.player = self.p1
        elif self.phase == len(self.PHASES)-1:
            self.player = self.p1 if self.player == self.p2 else self.p2
            self.phase = 0
        else:
            self.phase += 1


if __name__ == "__main__":
    Game()