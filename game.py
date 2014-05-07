from state import *
from Agent import *
from layout import getLayout
import time

BOARD = False
SCORE = True
WEIGHTS = False
SETUP = False
LEARN = True

class Game:
    def __init__(self, agents, startAgentIndex):
        self.agents = agents
        self.startAgentIndex = startAgentIndex

        self.gameOver = False

        self.agent0wins = 0
        self.agent1wins = 0

        self.num2000turns = 0


    def run(self):
        agentIndex = self.startAgentIndex

        agent0setup = self.agents[0].makeSetup()
        agent1setup = self.agents[1].makeSetup()

        self.state = GameState(getLayout("smallGrid.lay"),agent0setup, agent1setup)

        turns = 0

        if SETUP:
            self.state.prnt(0)

        while not self.gameOver:

            if self.state.isWon(0):
                #print "Player 0 wins!"
                self.agent0wins += 1
                print "Turns", turns
                break
            if self.state.isWon(1):
                #print "Player 1 wins!"
                self.agent1wins += 1
                print "Turns", turns
                break
           # agent.final(self.state)

            if turns > 2000:
                print "Turns", turns
                self.num2000turns += 1
                break

            turns += 1
            agent = self.agents[agentIndex]

           # print '\n'
           # print "AGENT", agent.index, "'s TURN"
           # print "--------------\n"

            action = agent.getAction(self.state)
            (piece, pos) = action
          #  print "ACTION:", (str(piece), piece.position, pos)

            nextState = self.state.getSuccessor(agentIndex, action)
            if LEARN:
                agent.update(self.state, action, nextState)
            self.state = nextState

            if BOARD and agentIndex == 0:
                self.state.prnt(agent.index)

            

            agentIndex = 1-agentIndex
            if BOARD: time.sleep(0.02)
        #print "The game took", turns, "turns."
        self.agents[0].final(self.state)
        self.agents[1].final(self.state)

def main():
    agent0 = ApproximateQAgent(0, epsilon=0.5, alpha=0.2)
    agent1 = RandomAgent(1)

    game = Game([agent0, agent1], 0)

    # weights after 5100 games (can see opponents pieces)
    #newdict = {'mysumofpiecesrows': -0.4074917633967522, 'yourpiecesum': 0.2139136270049274, 'numbombdiffusers': 0.3198096780820665, 'numbombs': -0.01758883640141232, 'flagsurrounded': -0.02395574694873867, 'yournumpieces': -0.01078281998170093, 'mynumpieces': 0.5385217847461586, 'distflagenemy': 1.0, 'mypiecesum': 0.5631366846940973, 'yoursumofpiecesrows': -0.03561273951110605}
    
    #weights after 1000 games (can't see opponents pieces)
    #newdict = {'mysumofpiecesrows': 0.14304587420030987, 'yourpiecesum': -1.0, 'numbombdiffusers': 0.8938795583712001, 'numbombs': 0.6811353507526687, 'flagsurrounded': -0.012575587571356493, 'yournumpieces': -0.8660935280072104, 'mynumpieces': 0.3083832947121093, 'distflagenemy': -0.6397444402906379, 'mypiecesum': -0.1441279138977027, 'yoursumofpiecesrows': -0.2959174092410362}
    # weights after 2000 games
    # newdict = {'mysumofpiecesrows': 0.03513988390360605, 'yourpiecesum': -1.0, 'numbombdiffusers': 0.7180310307185394, 'numbombs': 0.5272635675593819, 'flagsurrounded': -0.012513712847765595, 'yournumpieces': -0.8475237035193617, 'mynumpieces': 0.17497789779703374, 'distflagenemy': -0.6637231203153648, 'mypiecesum': -0.2267032554252376, 'yoursumofpiecesrows': -0.2903112564848997}
    # newdict = {'numbombs': -0.7475761386392166, 'yourpiecesum': -0.19471197711879412, 'numbombdiffusers': 0.2210793823655118, 'mysumofpiecesrows': -0.028286315814823174, 'iwon': 4.86422826341377e-05, 'flagsurrounded': -0.05793042061015382, 'yournumpieces': -0.7539541122967902, 'mynumpieces': 1.0, 'distflagenemy': -0.18757118464717795, 'mypiecesum': -0.2128251588143957, 'yoursumofpiecesrows': -0.5720138911234868, 'youwon': -4.86422826341377e-05}
    # for key, value in newdict.iteritems():
    #     game.agents[0].weights[key] = value

    wi = agent0.weights.copy()
    print "Initial weights", wi
    for i in range(5000):
        game.run()
        if (i%1 == 0):
            if WEIGHTS:
                print "Agent 0 Weights after game", i, " are", agent0.weights
                # print "Agent 1 Weights after game", i, " are", agent1.weights
            if SETUP:
                print "Agent 0 Setup Weights after game", i, " are", agent0.setupWeights, "\n"
            if SCORE:
                print "Player 0 won", game.agent0wins, "times"
                print "Player 1 won", game.agent1wins, "times"
                print "Num 2000 turns", game.num2000turns
            print
        if BOARD: time.sleep(5)
    print "Initial weights", wi
    print "Final weights", agent0.weights
    print "Player 0 won", game.agent0wins, "times"
    print "Player 1 won", game.agent1wins, "times"
    print "Num 2000 turns", game.num2000turns


if __name__ == "__main__": main()
