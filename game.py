from enum import Enum
from random import randint
from sub import Sub
from constants import Player, Direction, ALPHA_BOARD, Power


class Phase(Enum):
    Starting = "starting phase"
    Choose_Power = "choose power phase"
    Aim_Powers = "aim power phase"
    Movement = "movement phase"
    Breakdown = "breakdown phase"
    Mark_Power = "mark power phase"


class Game:

    PHASES = [Phase.Choose_Power, Phase.Movement, Phase.Breakdown, Phase.Mark_Power, Phase.Choose_Power]
    p1: Sub
    p2: Sub
    player: Sub
    phase: Phase
    phase_num: int
    board: tuple[tuple[int]]
    declared_direction: Direction
    action_used: bool
    

    def __init__(self):
        self.reset()


    def reset(self):
        self.history = []
        self.p1 = Sub(Player.One)
        self.p2 = Sub(Player.Two)
        self.player = self.p1
        self.phase = Phase.Starting
        self.phase_num = None
        self.board = ALPHA_BOARD
        self.declared_direction = None
        self.action_used = None

    
    def step(self, action):
        observation, reward, done = None, None, None
        if self.phase == Phase.Starting:
            self.player.set_starting_loc(action)
        elif self.phase == Phase.Choose_Power:
            if action is not None:
                self.handle_power(action)
                self.action_used = True
            else:
                self.action_used = False
        elif self.phase == Phase.Movement:
            self.player.move(action)
            self.declared_direction = action
        elif self.phase == Phase.Breakdown:
            self.player.breakdown(action, self.declared_direction)
        elif self.phase == Phase.Mark_Power:
            self.player.mark(action)
        else:
            raise Exception("phase not found")
        self.next_phase()

    
    def legal_actions(self):
        if self.phase == Phase.Starting:
            actions = []
            for row in range(len(self.board)):
                for col in range(len(self.board[0])):
                    if self.board[row][col] == 0:
                        actions.append((row,col))
            return actions
        elif self.phase == Phase.Choose_Power:
            return self.player.get_active_powers()
        elif self.phase == Phase.Movement:
            return self.player.get_valid_directions(self.board)
        elif self.phase == Phase.Breakdown:
            return self.player.get_unbroken_breakdowns(self.declared_direction)
        elif self.phase == Phase.Mark_Power:
            return self.player.get_unmarked_powers()
        else:
            raise Exception("phase not found")


    def next_phase(self):
        """
        Changes the current phase to the next one.
        Also changes current player to other one if its the end of the last phase.
        """
        if self.phase == Phase.Starting:
            assert self.phase_num == None, "phase is starting but phase_num is not none"
            if self.player == self.p1:
                self.player = self.p2
            else:
                assert self.player == self.p2, "player is not p1 or p2 in starting phase"
                self.phase_num = 0
                self.phase = self.PHASES[self.phase_num]
                self.player = self.p1
        elif self.action_used:
            pass
        elif self.phase_num == len(self.PHASES)-1:
            self.player = self.p1 if self.player == self.p2 else self.p2
            self.phase_num = 0
            self.phase = self.PHASES[self.phase_num]
        else:
            self.phase_num += 1
            self.phase = self.PHASES[self.phase_num]

    
    def handle_power(self, power):
        if power == Power.Drone:
            opponent = self.p1 if self.player == self.p1 else self.p2
            return opponent.get_quadrant(self.board)
        elif power == Power.Silence:
            pass
        elif power == Power.Torpedo:
            pass
        else:
            raise Exception("power not found")


if __name__ == "__main__":
    g = Game()
    while True:
        print("---------------------------------------")
        print(f"player: {g.player.player}")
        options = g.legal_actions()
        print(g.phase)
        print(options)
        action = randint(0,len(options)-1)
        g.step(options[int(action)])