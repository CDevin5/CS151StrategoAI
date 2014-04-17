# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


#from game import *
from LearningAgents import ReinforcementAgent
from featureExtractors import *
from piece import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.qValues = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.qValues[(state, action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return 0.0
        values = [self.getQValue(state, action) for action in actions]
        return max(values)

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return None
        values = [self.getQValue(state, action) for action in actions]
        LoT = zip(values, actions)
        (bestValue, bestAction) = max(LoT)
        return bestAction

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
            return None
        elif util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            return self.getPolicy(state)

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
      #  print "update"
        oldValue = self.getQValue(state, action)
        sample = reward + self.discount*self.computeValueFromQValues(nextState)
        self.qValues[(state, action)] = (1-self.alpha)*oldValue + self.alpha*(sample)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class ApproximateQAgent(QLearningAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, index, numTraining=10000, epsilon=0.5, alpha=0.5, gamma=0.5):
        self.featExtractor = FeatureExtractors()
        self.weights = util.Counter()
        featsList = self.featExtractor.getListOfFeatures()
        # for f in featsList:
        #     self.weights[f] = random.random()
        self.index = index
        QLearningAgent.__init__(self, numTraining=10000, epsilon=0.5, alpha=0.5, gamma=1)

    def makeSetup(self):
        """ Returns a list of pieces"""
        startingRanks = [FLAG, SPY, SCOUT, SCOUT, MINER, MINER, GENERAL, MARSHALL, BOMB, BOMB]
        startingSpots = random.sample(self.getStartSpots(), len(startingRanks))
        pieces = []
        for i in range(len(startingRanks)):
            pieces += [Piece(startingRanks[i], startingSpots[i], self.index)]
     #   print [(str(p), p.position) for p in pieces]
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


    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
       # print "getQValue"
        features = self.featExtractor.getFeatures(state, self.index)#.values()
        #weights = self.weights.values()
        #dotProduct = reduce( (lambda x, y: x*y), map( (lambda x, y: x+y), self.weights, features))
        #return dotProduct
        score = 0
        for key in features.keys():
            score += features[key]*self.weights[key]
        return score

    def compValFromState(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
      #  print "compValFromState"
        #actions = self.getLegalActions(state)
        # if len(actions) == 0:
        #     return 0.0
        # values = [self.getQValue() for action in actions]
        return self.getQValue(state, None)


    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
       # print "Update"
        difference = (reward + self.discount*self.compValFromState(nextState)) - self.getQValue(state, action)
        features = self.featExtractor.getFeatures(state, self.index)
        #print "features", features, "difference", difference, "weights", self.weights
        for key in self.weights:
            self.weights[key] = self.alpha * difference * features[key]
       # print "NEW WEIGHTS", self.weights      

    def final(self, state):
        "Called at the end of each game."
       # print "FINAL"
        # call the super-class final method
        QLearningAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
    def getScore(self, state):
        if state.isWon(self.index):
            return 10
        elif state.isWon(1-self.index):
            return -10
        else:
          return -1

