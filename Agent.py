import random
import state
from piece import *
from featureExtractors import *
import util

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

    def final(self, state):
        # Do nothing
        return

    def getStartSpots(self):
        """ Generates a list of the positions available for initial setup """
        spots = []
        if self.index == 0:
            startRow = 1
            endRow = 4
        if self.index == 1:
            startRow = 6
            endRow = 9
        for row in range(startRow, endRow):
            for col in range(1,9):
                spots += [(col, row)]
        return spots

    def makeSetup(self):
        """ Returns a list of pieces"""
        startingRanks = [FLAG, SPY, SCOUT, SCOUT, MINER, MINER, GENERAL, MARSHALL, BOMB, BOMB]
        startingSpots = random.sample(self.getStartSpots(), len(startingRanks))
        pieces = []
        for i in range(len(startingRanks)):
            pieces += [Piece(startingRanks[i], startingSpots[i], self.index)]
       # print [(str(p), p.position) for p in pieces]
        return pieces

class RandomAgent(Agent):
    """
    An agent that picks a random action.
    """
    def getAction(self, state):
        actions = state.getLegalActions(self.index)
        return random.choice(actions)
    

class HumanAgent(Agent):
    """
    An Agent that queries the user for an action
    """
    def getAction(self, state):
        piece = None
        newPos = None
        actions = state.getLegalActions(self.index)
        print "Legal actions:", [(str(p), p.position, pos) for (p, pos) in actions]
        while piece == None:
            print state
            userInput = raw_input("What is your move? (x0,y0) (x1,y1) ").split()
            oldList = list(userInput[0])
            oldPos = (int(oldList[1]), int(oldList[3]))
            newList = list(userInput[1])
            newPos = (int(newList[1]), int(newList[3]))
            piece = state.getPieceAtPos(oldPos)
            print "Old pos", oldPos
            print "New pos", newPos
            if piece == None:
                print "Invalid initial position"
            elif (piece, newPos) not in actions:
                print "Not a legal action"
                piece = None
            else:
                print "moving", piece, "from", oldPos, "to", newPos
        return (piece, newPos)

    def makeSetup(self):
        """ Returns a list of pieces"""
        startingRanks = [FLAG, SPY, SCOUT, SCOUT, MINER, MINER, GENERAL, MARSHALL, BOMB, BOMB]
        startingSpots = random.sample(self.getStartSpots(), len(startingRanks))
        pieces = []
        for i in range(len(startingRanks)):
            pieces += [Piece(startingRanks[i], startingSpots[i], self.index)]
        print [(str(p), p.position) for p in pieces]
        return pieces

    def getStartSpots(self):
        """ Generates a list of the positions available for initial setup """
        spots = []
        if self.index == 0:
            startRow = 1
            endRow = 4
        if self.index == 1:
            startRow = 6
            endRow = 9
        for row in range(startRow, endRow):
            for col in range(1,9):
                spots += [(col, row)]
        return spots

class ApproximateQAgent(Agent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, index, epsilon=0.5, alpha=0.5, gamma=0.5):
        self.featExtractor = FeatureExtractors()
        self.weights = util.Counter()
        featsList = self.featExtractor.getListOfFeatures()
        # for f in featsList:
        #     self.weights[f] = random.random()
        self.index = index
        self.exploreRate = epsilon
        self.learningRate = alpha
        self.discount = gamma

    def getAction(self, state):
        legalActions = state.getLegalActions(self.index)

        # Maybe Explore:
        r = random.random()
        if (r < self.exploreRate):
            return random.choice(legalActions)

        # Exploit:
        return max((self.getValue(state.getSuccessor(self.index, a)), a) for a in legalActions)[1]

    def getValue(self, state):
        """
          Should return V(state) = w * featureVector
          where * is the dotProduct operator
        """ 
        features = self.featExtractor.getFeatures(state, self.index)#.values()
        score = 0
        for key in features.keys():
            score += features[key]*self.weights[key]
        return score
