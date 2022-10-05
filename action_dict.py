from breakdowns import BreakdownMap
from constants import Direction, Power

def make_action_dict(board_x, board_y):
    action_dict = {}
    action_num = 0
    for x in range(board_x):
        for y in range(board_y):
            action_dict[(x,y)] = action_num
            action_num += 1
    for dir in Direction:
        action_dict[dir] = action_num
        action_num += 1
        # for silences
        for i in range(5):
            action_dict[(dir,i)] = action_num
            action_num += 1
    for power in Power:
        action_dict[power] = action_num
        action_num += 1
    breakdowns = BreakdownMap()
    for breakdown in breakdowns.all_breakdowns:
        action_dict[breakdown.__str__()] = action_num
        action_num += 1
    return action_dict