from enum import Enum
from random import randint
from sub import Sub
from constants import Player, Direction, ALPHA_BOARD, Power
import pygame as pg


class Phase(Enum):
    Starting = 1
    Choose_Power = 2
    Aim_Power = 3
    Movement = 4
    Breakdown = 5
    Mark_Power = 6


class BoardNumDisplay(Enum):
    Breakdowns = 1
    Powers = 2


class Game:

    PHASES = [Phase.Choose_Power, Phase.Movement, Phase.Breakdown, Phase.Mark_Power, Phase.Choose_Power]
    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 1500
    BOARD_FRAC_OF_DISPLAY = 4
    p1: Sub
    P1_COLOR = (0,0,0)
    p2: Sub
    P2_COLOR = (255,0,0)
    player: Sub
    phase: Phase
    phase_num: int
    board: tuple[tuple[int]]
    declared_direction: Direction
    power_to_aim: Power
    does_draw: bool
    screen: pg.Surface
    p1_last_actions: list
    p2_last_actions: list
    

    def __init__(self, does_draw = False):
        self.does_draw = does_draw
        if self.does_draw:
            pg.init()
            self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.reset()


    @property
    def opponent(self):
        return self.p2 if self.player == self.p1 else self.p1


    def reset(self):
        self.history = []
        self.board = ALPHA_BOARD
        self.p1 = Sub(Player.One, self.board)
        self.p2 = Sub(Player.Two, self.board)
        self.player = self.p1
        self.phase = Phase.Starting
        self.phase_num = None
        self.declared_direction = None
        self.power_to_aim = None
        self.p1_last_actions = []
        self.p2_last_actions = []
        if self.does_draw:
            self.draw_all_boards()


    def draw_all_boards(self):
        self.screen.fill((0,0,0))
        self.setup_boards("C:/Users/jerem/Documents/GitHub/Captain-Sonar/powers.png", BoardNumDisplay.Powers)
        self.setup_boards("C:/Users/jerem/Documents/GitHub/Captain-Sonar/breakdowns.png", BoardNumDisplay.Breakdowns)
        self.setup_map("C:/Users/jerem/Documents/GitHub/Captain-Sonar/alpha_map.png")


    def setup_map(self, path):
        board = pg.image.load(path).convert()
        board = pg.transform.scale(board, (self.SCREEN_WIDTH//(self.BOARD_FRAC_OF_DISPLAY//2), self.SCREEN_HEIGHT))
        self.screen.blit(board, (0,0))
    

    def setup_boards(self, path, board_type):
        for height in [0, self.SCREEN_HEIGHT//2]:
            breakdown = pg.image.load(path).convert()
            breakdown = pg.transform.scale(breakdown, (self.SCREEN_WIDTH//self.BOARD_FRAC_OF_DISPLAY, self.SCREEN_HEIGHT//2))
            self.screen.blit(breakdown,(self._get_secondary_board_x(board_type), height))


    def _get_secondary_board_x(self, board_type):
        return (self.SCREEN_WIDTH//self.BOARD_FRAC_OF_DISPLAY)*(self.BOARD_FRAC_OF_DISPLAY-board_type.value)


    def update_display(self):
        self.draw_all_boards()
        self._pg_update_breakdowns()
        self._pg_update_powers()
        self._pg_update_damage()
        self._pg_update_player_pos_and_path()
        pg.display.flip()
        pass

    
    def step(self, action):
        if self.phase == Phase.Starting:
            self.player.set_starting_loc(action)
        elif self.phase == Phase.Choose_Power:
            if action is not None:
                self.player.powers[action] = 0
                if action == Power.Drone:
                    opponent = self.opponent
                    observation = opponent.get_quadrant() # TODO: observation
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
        if self.player == self.p1:
            self.p1_last_actions.append(action)
        else:
            assert self.player == self.p2, "player is not p1 or p2"
            self.p2_last_actions.append(action)
        self.next_phase()
        observation = self._get_observation()
        reward = self.opponent.damage - self.player.damage
        done = self.player.damage >= 4 or self.opponent.damage >= 4
        if self.does_draw:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    raise KeyboardInterrupt()
            self.update_display()
        return observation, reward, done

    
    def _get_observation(self):
        """Things to go in the observation:
        your damage
        opponents damage
        your location row
        your location col
        current phase num
        your breakdowns
        all actions opponent used on their last turn
        # TODO: dont add certain things to last_actions
            like starting pos, breakdown, power mark

        maybe to add:
        your power marks??
        the map??
        """
        observation = [
            self.player.damage,
            self.opponent.damage,
            self.player.loc[0],
            self.player.loc[1],
            self.phase.value,
        ]
        for breakdown in self.player.breakdownMap.all_breakdowns:
            representation = int(breakdown.__repr__())
            observation.append(int(representation))
        if self.player == self.p1:
            observation += self.p2_last_actions
        else:
            assert self.player == self.p2, "player not p1 or p2"
            observation += self.p1_last_actions
        return observation

    
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
            return self.player.get_valid_directions()
        elif self.phase == Phase.Breakdown:
            return self.player.get_unbroken_breakdowns(self.declared_direction)
        elif self.phase == Phase.Mark_Power:
            return self.player.get_unmarked_powers()
        elif self.phase == Phase.Aim_Power:
            return self.player.get_power_options(self.power_to_aim)
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
            if self.player == self.p1:
                self.p2_last_actions = []
            else:
                assert self.player == self.p2, "player is not p1 or p2"
                self.p1_last_actions = []
            self.player = self.opponent
            self.phase_num = 0
            self.phase = self.PHASES[self.phase_num]
        else:
            self.phase_num += 1
            self.phase = self.PHASES[self.phase_num]


    def handle_power(self, action):
        # TODO: draw powers to screen
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
                p.damage += 1
            prow, pcol = p.loc
            if abs(prow-row) <= 1 and abs(pcol-col) <= 1:
                p.damage += 1


    def _pg_update_player_pos_and_path(self):
        x = lambda x: self.SCREEN_WIDTH/23 + x*self.SCREEN_WIDTH/49.7
        y = lambda y: self.SCREEN_HEIGHT/6.1 + y*self.SCREEN_HEIGHT/18.7
        l = [(self.p1, self.P1_COLOR, 0), (self.p2, self.P2_COLOR, self.SCREEN_HEIGHT*0.008)]
        for player, color, offset in l:
            if player.loc:
                rec = pg.Rect(x(player.loc[1])+offset, y(player.loc[0])+offset, self.SCREEN_WIDTH/80, self.SCREEN_HEIGHT/40)
                pg.draw.rect(self.screen, color, rec)
        # update paths of subs
        for player, color, offset in l:
            for row, col in player.path:
                rec = pg.Rect(x(col)+offset, y(row)+offset, self.SCREEN_WIDTH/160, self.SCREEN_HEIGHT/80)
                pg.draw.rect(self.screen, color, rec)


    def _pg_update_damage(self):
        for damage, height, color in [(self.p1.damage, 0, self.P1_COLOR), (self.p2.damage, self.SCREEN_HEIGHT/2, self.P2_COLOR)]:
            x = self._get_secondary_board_x(BoardNumDisplay.Powers)*1.349
            for _ in range(damage):
                rec = pg.Rect(x, height+self.SCREEN_HEIGHT*0.068, self.SCREEN_WIDTH/100, self.SCREEN_HEIGHT/50)
                x += rec.width + self.SCREEN_WIDTH*0.005
                pg.draw.rect(self.screen, color, rec)


    def _pg_update_breakdowns(self):
        direction_locs = {
            Direction.West: 0,
            Direction.North: 1,
            Direction.South: 2,
            Direction.East: 3
        }
        direction_layouts = {
            # row, col where each breakdown is within the direction
            Direction.West: ((0,0),(0,2),(1,2),(2,0),(2,1),(2,2)),
            Direction.North: ((0,0),(1,0),(1,2),(2,0),(2,1),(2,2)),
            Direction.South: ((0,0),(1,0),(1,2),(2,0),(2,1),(2,2)),
            Direction.East: ((0,0),(1,0),(1,2),(2,0),(2,1),(2,2))
        }
        x = lambda dir: self._get_secondary_board_x(BoardNumDisplay.Breakdowns) + self.SCREEN_WIDTH*direction_locs[dir]*0.0496 + self.SCREEN_WIDTH*0.0335
        for player, color, height in [(self.p1, self.P1_COLOR, 0), (self.p2, self.P2_COLOR, self.SCREEN_HEIGHT/2)]:
            num_in_class = 0
            prev_dir = None
            for breakdown in player.breakdownMap.all_breakdowns:
                dir = breakdown.direction_class
                if not prev_dir == dir:
                    prev_dir = dir
                    num_in_class = 0
                if breakdown.marked:
                    rec = pg.Rect(x(dir)+(direction_layouts[dir][num_in_class][1]*self.SCREEN_WIDTH*0.014), self.SCREEN_HEIGHT*0.285+height+(0.049*self.SCREEN_HEIGHT*direction_layouts[dir][num_in_class][0]), self.SCREEN_WIDTH/100, self.SCREEN_HEIGHT/50)
                    pg.draw.rect(self.screen, color, rec)
                num_in_class += 1


    def _pg_update_powers(self):
        # location out of the powers
        power_locs = {
            Power.Silence: (2,0),
            Power.Drone: (1,0),
            Power.Torpedo: (0,1),
        }
        x = lambda x: self._get_secondary_board_x(BoardNumDisplay.Powers) + self.SCREEN_WIDTH*0.052 + self.SCREEN_WIDTH*x*0.074
        y = lambda y: self.SCREEN_HEIGHT*y*0.18 + self.SCREEN_HEIGHT*0.125
        mark_offsets = {
            1: (0,0),
            2: (0.01, 0.027),
            3: (0.01, 0.063),
            4: (0, 0.088),
            5: (-0.014, 0.088),
            6: (-0.025, 0.063)
        }
        for player, color, height in [(self.p1, self.P1_COLOR, 0), (self.p2, self.P2_COLOR, self.SCREEN_HEIGHT/2)]:
            for power, marks in player.powers.items():
                assert marks <= 6, "cant have more than 6 marks on one power"
                for offset_num in range(1,marks+1,1):
                    x_offset_frac, y_offset_frac = mark_offsets[offset_num]
                    rec = pg.Rect(x(power_locs[power][0])+(x_offset_frac*self.SCREEN_WIDTH), y(power_locs[power][1])+height+(y_offset_frac*self.SCREEN_HEIGHT), self.SCREEN_WIDTH/100, self.SCREEN_HEIGHT/50)
                    pg.draw.rect(self.screen, color, rec)


if __name__ == "__main__":
    does_draw = True
    g = Game(does_draw)
    num_games = 0
    try:
        while True:
            print("---------------------------------------")
            print(f"player: {g.player.player}")
            options = g.legal_actions()
            print("options: ", options)
            if len(options) > 1 and g.phase in [Phase.Movement, Phase.Choose_Power]:
                action = randint(1,len(options)-1)
            else:
                action = randint(0,len(options)-1)
            obs, reward, done = g.step(options[int(action)])
            print("obs: ", obs)
            print("reward: ", reward)
            print("done: ", done)
            if done:
                g = Game(does_draw)
                num_games += 1
    finally:
        print(num_games)
        pg.quit()