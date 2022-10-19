from random import randint
from typing import Any

from game.breakdowns import BreakdownChannel, BreakdownMap
from actors.actor import Actor
from game.constants import Direction, Power
from game.sub import Sub


class Expert_Actor(Actor):
    
    def __init__(self, action_dict: dict[Any, int], reverse_action_dict: dict[int, Any], board: tuple[tuple[int]]):
        super().__init__(action_dict, reverse_action_dict, board)
        self.breakdowns_on_paths = set()
        self.breakdowns = BreakdownMap()
        self.examined_obs = set()

        self.possible_opp_positions: set[tuple[int, int]] = set()
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                self.possible_opp_positions.add((row, col))

        for breakdown in self.breakdowns.all_breakdowns:
            if breakdown.channel not in [BreakdownChannel.No_Channel, BreakdownChannel.Radiation]:
                self.breakdowns_on_paths.add(breakdown)


    def _choose_action(self, actions: list[int], obs: list[int]):

        self._update_possible_enemy_locs(obs)

        # if its choose power phase
        if obs[4] == 2:
            if self.action_dict[Power.Torpedo] in actions:
                torpedo_options = Sub.get_torpedo_options((obs[2], obs[3]), self.board) # TODO: account for splash dmg
                for option in torpedo_options:
                    if self._in_torpedo_range(option, (obs[2], obs[3])):
                        continue
                    if option in self.possible_opp_positions:
                        return self.action_dict[Power.Torpedo]
                actions.remove(self.action_dict[Power.Torpedo])

        # if its aim power phase
        if obs[4] == 3 and len(actions) > 1:
            # if its torpedo
            if isinstance(self.reverse_action_dict[actions[1]][0], int):
                for action in actions:
                    loc = self.reverse_action_dict[action]
                    if loc in self.possible_opp_positions and not self._in_torpedo_range(loc, (obs[2], obs[3])):
                        return action
                raise Exception("should know there is a place to hit when activating a torpedo")

        # if its mov phase
        elif obs[4] == 4 and len(actions) > 1:
            # TODO: use that model to get an average position of all the posiblities
            # use the std variation as a confidence
            # use that confidence as a weight for how much to weigh decideing to go in that direction
            # take that score in conjunction with the breakdowns to decide which direction to go

            # choose the direction with the least breakdowns
            num_marked = {}
            for i, action in enumerate(actions):
                direction = self.reverse_action_dict[action]
                for breakdown, marked in zip(self.breakdowns.all_breakdowns, obs[13:(13+len(self.breakdowns.all_breakdowns))]):
                    if not marked:
                        if breakdown.direction_class == direction:
                            num_marked[i] = num_marked.get(i, 0) + 1
            least_marked = -1
            best_dir = None
            for key, val in num_marked.items():
                if val > least_marked:
                    least_marked = val
                    best_dir = key
            # if we will take damage, surface instead
            if least_marked in [1,-1]:
                return actions[0]
            return actions[best_dir]

        # if its the breadkown phase
        elif obs[4] == 5 and len(actions) > 1:
            # priotitize breakdowns that are part of channels so we can increase clearing
            for i, action in enumerate(actions):
                if self.reverse_action_dict[action] in self.breakdowns_on_paths:
                    return actions[i]
        if len(actions) > 1 and obs and obs[4] in [4, 2]:
            action = randint(1,len(actions)-1)
        else:
            action = randint(0,len(actions)-1)
        return actions[action]


    def _update_possible_enemy_locs(self, current_obs):

        for obs in self.unexamined_first_phase_obs:
            self._update_possible_locs(obs)
        self.unexamined_first_phase_obs = []

        opp_quadrant = current_obs[5]
        to_remove = set()
        if not opp_quadrant == -1:
            for loc in self.possible_opp_positions:
                if not opp_quadrant == Sub.get_quadrant(loc, self.board):
                    to_remove.add(loc)
        self.possible_opp_positions -= to_remove


    def _update_possible_locs(self, obs):
        old_possible_locs = set(self.possible_opp_positions)

        opp_dir = obs[6]

        opp_torpedo_used = obs[7] # TODO: make better by using these
        opp_torpedo_row = obs[8]
        opp_torpedo_col = obs[9]

        opp_silence_used = obs[10]
        opp_silence_dir = obs[11]

        for loc in old_possible_locs:
            # 0 for silence, -1 for starting/silenced, 1,2,3,4 for directions
            assert not ((opp_dir > 0) and opp_silence_used), "should not be able to move and silence in the same turn"
            if opp_dir > 0:
                new_loc = Sub.get_coord_in_direction(loc, Direction(opp_dir))
                self.possible_opp_positions.remove(loc)
                if Sub.in_bounds(new_loc[0], new_loc[1], self.board) and self.board[new_loc[0]][new_loc[1]] == 0:
                    self.possible_opp_positions.add(new_loc)
            if opp_silence_used:
                new_possible_positions = set()
                for dir, num_moved in Sub.get_silence_options(loc, self.board, [], [Direction(opp_silence_dir)]): # can make better by adding possible paths for every possible loc
                    new_loc = loc
                    for _ in range(num_moved):
                        new_loc = Sub.get_coord_in_direction(new_loc, dir)
                    new_possible_positions.add(new_loc)
                self.possible_opp_positions = new_possible_positions


    def _in_torpedo_range(self, loc1, loc2):
        should_continue = False
        for i in range(-1,2):
            for j in range(-1,2):
                if loc1[0]+i == loc2[0] and loc1[1]+j == loc2[1]: should_continue = True
                if should_continue: continue
            if should_continue: continue
        return should_continue