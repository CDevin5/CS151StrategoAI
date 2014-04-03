import random

class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """
    def __init__(self, index=0):
        self.index = index

    def getAction(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        raiseNotDefined()

class RandomAgent(Agent):
    """
    An agent that picks a random action.
    """
    def getAction(self, state):
        actions = state.getLegalActions()
        return random.choice(legalActions)

class HumanAgent(Agent):
    """
    An Agent that queries the user for an action
    """
    def getAction(self, state):
        piece = None
        newPos = None
        while piece = None:
            print state
            userInput = raw_input("What is your move? [square of piece's current location] [square to move it to]").split()
            oldPos = userInput[0]
            newPos = userInput[1]
            piece = getPieceAtPos(self, oldPos):
            if piece == None:
                print "Invalid initial position"
            else print "moving", piece, "from", oldPos, "to", pos
        return (piece, newPos)

