from turn import Turn
from sub import Sub

class Sonar:

    history: list[Turn]
    p1 = None
    p2 = None
    
    def __init__(self, history: list[Turn], p1, p2):
        self.history = history
        self.p1 = p1 if p1 else Sub()
        self.p2 = p2 if p2 else Sub()

    
    def step():
        # ask player if they want to use a power
            # do the power if they do one
            # then ask for another (keep asking)
        # ask player to move (including surfacing)
        pass


if __name__ == "__main__":
    pass