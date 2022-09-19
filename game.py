from enum import Enum
from random import randint
from sub import Sub
from constants import Player, Direction, ALPHA_BOARD, Power


class Phase(Enum):
    Starting = "starting phase"
    Choose_Power = "choose power phase"
    Aim_Power = "do/aim power phase"
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
    power_to_aim: Power
    

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
        self.power_to_aim = None

    
    def step(self, action):
        observation = None # TODO: think of good observation
        if self.phase == Phase.Starting:
            self.player.set_starting_loc(action)
        elif self.phase == Phase.Choose_Power:
            if action is not None:
                if action == Power.Drone:
                    opponent = self.opponent
                    observation = opponent.get_quadrant(self.board) # TODO: observation
                else:
                    self.power_to_aim = action
        elif self.phase == Phase.Movement:
            self.player.move(action)
            self.declared_direction = action
        elif self.phase == Phase.Breakdown:
            self.player.breakdown(action, self.declared_direction)
        elif self.phase == Phase.Mark_Power:
            self.player.mark(action)
        elif self.phase == Phase.Aim_Power:
            observation = self.handle_power(action) # TODO: observation
            self.power_to_aim = None
        else:
            raise Exception("phase not found")
        self.next_phase()
        reward = self.opponent.damage - self.player.damage
        done = self.player.damage >= 4 or self.opponent.damage >= 4
        return observation, reward, done

    
    def legal_actions(self):
        if self.phase == Phase.Starting:
            actions = []
            for row in range(len(self.board)):
                for col in range(len(self.board[0])):
                    if self.board[row][col] == 0:
                        actions.append((row,col))
            return actions
        elif self.phase == Phase.Choose_Power:
            return self.player.get_active_powers(self.board)
        elif self.phase == Phase.Movement:
            return self.player.get_valid_directions(self.board)
        elif self.phase == Phase.Breakdown:
            return self.player.get_unbroken_breakdowns(self.declared_direction)
        elif self.phase == Phase.Mark_Power:
            return self.player.get_unmarked_powers(self.board)
        elif self.phase == Phase.Aim_Power:
            return self.player.get_power_options(self.power_to_aim, self.board)
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
        elif self.power_to_aim:
            self.phase = Phase.Aim_Power
        elif self.phase_num == len(self.PHASES)-1:
            self.player = self.opponent
            self.phase_num = 0
            self.phase = self.PHASES[self.phase_num]
        else:
            self.phase_num += 1
            self.phase = self.PHASES[self.phase_num]


    def handle_power(self, action):
        power = self.power_to_aim
        observation = None
        if power == Power.Silence:
            observation = action
            self.player.silence(action)
        elif power == Power.Torpedo:
            explosion_loc = action
            observation = explosion_loc
            self._explosion(explosion_loc)
        else:
            raise Exception("power not found")
        return observation


    def _explosion(self, loc):
        row, col = loc
        for p in [self.p1, self.p2]:
            if p.loc == loc:
                p.damage += 2
            prow, pcol = p.loc
            if abs(prow-row) <= 1 and abs(pcol-col) <= 1:
                p.damage += 1


    @property
    def opponent(self):
        return self.p1 if self.player == self.p1 else self.p2


if __name__ == "__main__":
    g = Game()
    while True:
        print("---------------------------------------")
        print(f"player: {g.player.player}")
        options = g.legal_actions()
        print(g.phase)
        print(options)
        action = randint(0,len(options)-1)
        print(action)
        obs, reward, done = g.step(options[int(action)])
        if done: g = Game()