import random
import state

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
        return random.choice(actions)
    def makeSetup(self):
        """ Returns a list of pieces"""
        startingRanks = [FLAG, SPY, SCOUT, SCOUT, MINER, MINER, GENERAL, MARSHALL, BOMB, BOMB]
        startingSpots = random.sample(self.getStartSpots(), len(startingRanks))
        pieces = []
        for i in len(startingRanks):
            pieces += [Piece(startingRanks[i], startingSpots[i], self.index)]
        return pieces

class HumanAgent(Agent):
    """
    An Agent that queries the user for an action
    """
    def getAction(self, state):
        piece = None
        newPos = None
        while piece == None:
            print state
            userInput = raw_input("What is your move? (x0,y0) (x1,y1) ").split()
            oldList = list(userInput[0])
            oldPos = (oldList[1], oldList[3])
            newList = list(userInput[1])
            newPos = (newList[1], newList[3])
            piece = state.getPieceAtPos(self, oldPos)
            if piece == None:
                print "Invalid initial position"
            else:
                print "moving", piece, "from", oldPos, "to", pos
        return (piece, newPos)

    def makeSetup(self):
        """ Returns a list of pieces"""
        startingRanks = [FLAG, SPY, SCOUT, SCOUT, MINER, MINER, GENERAL, MARSHALL, BOMB, BOMB]
        startingSpots = random.sample(self.getStartSpots(), len(startingRanks))
        pieces = []
        for i in len(startingRanks):
            pieces += [Piece(startingRanks[i], startingSpots[i], self.index)]
        return pieces

