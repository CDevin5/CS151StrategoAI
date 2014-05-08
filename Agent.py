import random
import state
from piece import *
from featureExtractors import *
import util
import copy

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

    def update(self, state, action, nextState):
        return

    def final(self, state):
        return

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
    def __init__(self, index, epsilon=0.5, alpha=0.5, gamma= 0.999):
        self.featExtractor = FeatureExtractors()
        self.setupFeatExtractor = SetupFeatures()
        self.weights = util.Counter()
        self.setupWeights = util.Counter()
        featsList = self.featExtractor.getListOfFeatures()
        # for f in featsList:
        #     self.weights[f] = 0#random.random()
        self.index = index
        self.exploreRate = epsilon
        self.learningRate = alpha
        self.discount = gamma
        

    def getAction(self, state):
        legalActions = state.getLegalActions(self.index)
        if legalActions == []:
            return None
        # Maybe Explore:
        r = random.random()
        if (r < self.exploreRate):
            return random.choice(legalActions)

        # Exploit:
        return max((self.getQValue(state, a), a) for a in legalActions)[1]

    def getValue(self, state):
        """
          Should return V(state) = w * featureVector
          where * is the dotProduct operator
        """ 
        features = self.featExtractor.getFeatures(state, self.index)
        score = 0
        for key in features.keys():
            score += features[key]*self.weights[key]
        return score

    def getQValue(self, state, action):
        if action == None:
            return self.getReward(state)
        stateProbs = state.getSuccessorsProbs(self.index, action)
        return sum(self.getValue(s)*p for (s, p) in stateProbs)

    def update(self, state, action, nextState):
        """
           Should update your weights based on transition
        """
        reward = self.getReward(nextState)
        difference = (reward + self.discount*self.getQValue(nextState, self.getAction(nextState))) - self.getQValue(state, action)
        features = self.featExtractor.getFeatures(state, self.index)
        for key in self.weights:
            # divisor = max(abs(self.weights[key]), abs(self.weights[key]+1))
            self.weights[key] += (self.learningRate * difference * features[key])#+(1-self.learningRate)*self.weights[key])/(divisor)
        maxVal = max(abs(v) for v in self.weights.values())
        if maxVal != 0:
            self.weights.divideAll(maxVal)

    def updateSetupWeights(self, reward):
        difference = reward - self.getSetupValue(self.finalSetup)
        features = self.setupFeatExtractor.getFeatures(self.finalSetup)
        for key in self.setupWeights:
            divisor = max(abs(self.setupWeights[key]), abs(self.setupWeights[key]+1))
            self.setupWeights[key] += (self.learningRate * difference * features[key])#+(1-self.learningRate)*self.weights[key])/(divisor)
        maxVal = max(abs(v) for v in self.setupWeights.values())
        if maxVal != 0:
            self.setupWeights.divideAll(maxVal)
        
    def getReward(self, nextState):
        if nextState.isWon(self.index):
            return 2
        elif nextState.isWon(1-self.index):
            return -1
        else:
          return -0.001

    def getLegalPlacements(self, pieces):
        legalPlacements = self.getStartSpots()

        for p in pieces:
            legalPlacements.remove(p.position)
        return legalPlacements

    def getLocation(self, rank, piecesPlaced):
        legalPlacements = self.getLegalPlacements(piecesPlaced)
        if legalPlacements == []:
            return None
        # Maybe Explore:
        r = random.random()
        if (r < self.exploreRate):
            return random.choice(legalPlacements)

        # Exploit:
        return max((self.getSetupQValue(piecesPlaced, (pos, rank)), pos) for pos in legalPlacements)[1]

    def getSetupValue(self, pieces):
        features = self.setupFeatExtractor.getFeatures(pieces)
        score = 0
        for key in features.keys():
           # print key, "value:", features[key], "weight", sel
            score += features[key]*self.setupWeights[key]
        return score

    def getSetupQValue(self, pieces, action):
        (pos, rank) = action
        newPiece = Piece(rank, pos, self.index)
        piecesCopy = copy.deepcopy(pieces)
        piecesCopy.append(newPiece)
        return self.getSetupValue(piecesCopy)

    def makeSetup(self):
        """ Returns a list of pieces"""
        piecesPlaced = []
        startingRanks = [FLAG, BOMB, BOMB, SPY, SCOUT, SCOUT, MINER, MINER, GENERAL, MARSHALL]
        
        for rank in startingRanks:
            piecesPlaced.append(Piece(rank, self.getLocation(rank, piecesPlaced), self.index))

        self.finalSetup = piecesPlaced

        return piecesPlaced

    def final(self, state):
        if state.isWon(self.index):
            self.updateSetupWeights(1)
        else:
            self.updateSetupWeights(-1)

