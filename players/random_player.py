from random import randint

def choose_action(actions, obs):
    # if phase is mov or choose power, dont do nothing
    if len(actions) > 1 and obs and obs[4] in [4, 2]:
        action = randint(1,len(actions)-1)
    else:
        action = randint(0,len(actions)-1)
    return action