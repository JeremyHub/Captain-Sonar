from random import randint
from typing import Any

from game.breakdowns import BreakdownChannel, BreakdownMap, BreakdownType
from actors.actor import Actor
from game.constants import DIRECTION_COORDS, Direction, Power
from game.sub import Sub


class Expert_Actor(Actor):
    
    def __init__(self, action_dict: dict[Any, int], reverse_action_dict: dict[int, Any], board: tuple[tuple[int]]):
        super().__init__(action_dict, reverse_action_dict, board)
        self.breakdowns = BreakdownMap()
        self.examined_obs = set()
        self.average_enemy_loc = (-1,-1)
        self.used_torpedo = False
        self.used_torpedo_loc = None
        self.prev_opp_dmg = None

        self.possible_opp_positions: set[tuple[int, int]] = set()
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    self.possible_opp_positions.add((row, col))


    def _choose_action(self, actions: list[int], obs: list[int]):

        if self.unexamined_first_phase_obs:
            self.used_torpedo = False
            self.used_torpedo_loc = None
            self.prev_opp_dmg = obs[1]

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

        # if its mark power phase
        elif obs[4] == 6:
            if self.action_dict[Power.Torpedo] in actions:
                return self.action_dict[Power.Torpedo]

        # if its aim power phase
        elif obs[4] == 3 and len(actions) > 1:
            # if its torpedo
            test_action = self.reverse_action_dict[actions[1]]
            if isinstance(test_action, tuple) and len(test_action) == 2 and isinstance(test_action[0], int):
                possibilities = []
                for action in actions:
                    loc = self.reverse_action_dict[action]
                    if not self._in_torpedo_range(loc, (obs[2], obs[3])):
                        possibilities.append((action, loc))
                for possibility, loc in possibilities:
                    if loc in self.possible_opp_positions:
                        self.used_torpedo = True
                        self.used_torpedo_loc = loc
                        return possibility
                raise Exception("should know there is a place to hit when activating a torpedo")

        # if its mov phase
        elif obs[4] == 4 and len(actions) > 1:
            # TODO: use the std variation as a confidence
            # use that confidence as a weight for how much to weigh decideing to go in that direction
            # take that score in conjunction with the breakdowns to decide which direction to go

            avg_point = self._get_average_point(self.possible_opp_positions)
            self.average_enemy_loc = avg_point
            vector_to_avg_enemy_pos = ((obs[2] - avg_point[0]), (obs[3] - avg_point[1]))
            vector_to_avg_enemy_pos = (round(vector_to_avg_enemy_pos[0]/abs(vector_to_avg_enemy_pos[0]+0.001)),round(vector_to_avg_enemy_pos[1]/abs(vector_to_avg_enemy_pos[1]+0.001)))

            # choose the direction with the least breakdowns
            num_marked = {}
            for action in actions:
                direction = self.reverse_action_dict[action]
                for breakdown, marked in zip(self.breakdowns.all_breakdowns, obs[13:(13+len(self.breakdowns.all_breakdowns))]):
                    assert marked in [0,1]
                    if not marked:
                        if breakdown.direction_class == direction:
                            num_marked[direction] = num_marked.get(direction, 0) + 1
            best_dirs = []
            most_unmarked = -1
            for key, val in num_marked.items():
                if val > most_unmarked:
                    most_unmarked = val
                    best_dirs = [key]
                elif val == most_unmarked:
                    best_dirs.append(key)
            # if we will take damage, surface instead
            if most_unmarked in [1,-1]:
                return actions[0]
            
            best_dirs_in_direction = []
            for dir in best_dirs:
                dir_vector = DIRECTION_COORDS[dir]
                if dir_vector == vector_to_avg_enemy_pos:
                    return self.action_dict[dir]
                elif (dir_vector[0] == vector_to_avg_enemy_pos[0] and not dir_vector[0] == 0) or (dir_vector[1] == vector_to_avg_enemy_pos[1] and not dir_vector[1] == 0):
                    best_dirs_in_direction.append((1,dir))
                else:
                    best_dirs_in_direction.append((0,dir))
            best_dirs_in_direction.sort(key=lambda x: x[0], reverse=True)
            if best_dirs_in_direction:
                return self.action_dict[best_dirs_in_direction[0][1]]

        # if its the breadkown phase
        elif obs[4] == 5 and len(actions) > 1:
            # priotitize breakdowns that are part of channels so we can increase clearing
            # also prioritize no red type breakdowns and no radiation
            good_breakdowns = []
            
            for action in actions:
                if not self.reverse_action_dict[action].channel == BreakdownChannel.No_Channel:
                    good_breakdowns.append((2, action))
                    if not self.reverse_action_dict[action].channel == BreakdownChannel.Radiation:
                        good_breakdowns.append((1, action))
                        # check if marking this would mean all the other breakdowns in the channel are marked
                        for breakdown, marked in zip(self.breakdowns.all_breakdowns, obs[13:(13+len(self.breakdowns.all_breakdowns))]):
                            if breakdown.channel == self.reverse_action_dict[action].channel and not marked:
                                break
                        else:
                            return action
                        if not self.reverse_action_dict[action].type == BreakdownType.Red:
                            return action
            if good_breakdowns:
                good_breakdowns.sort(key = lambda x: x[0])
                return good_breakdowns[0][1]

        # if we get to here just do something random
        # if its mov or power phase dont do nothing
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
        opp_surface_quadrant = current_obs[11]

        if opp_quadrant > -1 and opp_surface_quadrant > -1:
            assert opp_quadrant == opp_surface_quadrant, "surface quadrant and drone quadrant should match"
        
        to_remove = set()

        if not opp_quadrant == -1 or not opp_surface_quadrant == -1:
            quad = opp_quadrant if not opp_quadrant == -1 else opp_surface_quadrant
            for loc in self.possible_opp_positions:
                if not quad == Sub.get_quadrant(loc, self.board):
                    to_remove.add(loc)

        if self.used_torpedo:
            diff_opp_dmg = current_obs[1] - self.prev_opp_dmg
            # if we hit the enemy
            if diff_opp_dmg > 0:
                if diff_opp_dmg == 2:
                    self.possible_opp_positions = set([self.used_torpedo_loc])
                else:
                    for loc in self.possible_opp_positions:
                        if not self._in_torpedo_range(loc, self.used_torpedo_loc):
                            to_remove.add(loc)
            # otherwise, the torpedo missed
            else:
                for loc in self.possible_opp_positions:
                    if self._in_torpedo_range(loc, self.used_torpedo_loc):
                        to_remove.add(loc)

        self.possible_opp_positions -= to_remove

        assert self.possible_opp_positions, "there should always be at least one spot where it could be"


    def _update_possible_locs(self, obs):

        opp_dir = obs[6]

        opp_torpedo_used = obs[7] # can make better by using these, the problem is we dont know if they used it before or after they moved
        opp_torpedo_row = obs[8]
        opp_torpedo_col = obs[9]

        opp_silence_used = obs[10]

        new_possible_positions = set()

        assert not ((opp_dir >= 0) and opp_silence_used), "should not be able to move/surface and silence in the same turn"
        for loc in self.possible_opp_positions:
            # 0 for surface, -1 for starting/silenced, 1,2,3,4 for directions
            if opp_dir > 0:
                new_loc = Sub.get_coord_in_direction(loc, Direction(opp_dir))
                if Sub.in_bounds(new_loc[0], new_loc[1], self.board) and self.board[new_loc[0]][new_loc[1]] == 0:
                    new_possible_positions.add(new_loc)

            elif opp_silence_used:
                assert opp_dir == -1, "opp silence true but dir was not -1"
                for dir, num_moved in Sub.get_silence_options(loc, self.board, []): # can make better by adding possible paths for every possible loc
                    new_loc = loc
                    for _ in range(num_moved):
                        new_loc = Sub.get_coord_in_direction(new_loc, dir)
                    new_possible_positions.add(new_loc)

            else:
                # the sub was sufraced
                assert opp_dir == 0 or opp_dir == -1, "didnt move or use silence but didnt surface"
                return

        self.possible_opp_positions = new_possible_positions


    def _in_torpedo_range(self, loc1, loc2):
        should_continue = False
        for i in range(-1,2):
            for j in range(-1,2):
                if loc1[0]+i == loc2[0] and loc1[1]+j == loc2[1]: should_continue = True
                if should_continue: continue
            if should_continue: continue
        return should_continue


    def _get_average_point(self, points):
        total_x = 0
        total_y = 0
        for x, y in points:
            total_x += x
            total_y += y
        return (total_x/len(points), total_y/len(points))