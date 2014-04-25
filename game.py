from state import *
from Agent import *
from layout import getLayout

class Game:
    def __init__(self, agents, startAgentIndex):
        self.agents = agents
        self.startAgentIndex = startAgentIndex

        self.gameOver = False

        self.agent0wins = 0
        self.agent1wins = 0


    def run(self):
        agentIndex = self.startAgentIndex

        agent0setup = self.agents[0].makeSetup()
        agent1setup = self.agents[1].makeSetup()

        self.state = GameState(getLayout("smallGrid.lay"),agent0setup, agent1setup)

        turns = 0

        # weights after 5100 games.
        newdict = {'mysumofpiecesrows': 0.4074917633967522, 'yourpiecesum': 0.2139136270049274, 'numbombdiffusers': 0.3198096780820665, 'numbombs': -0.01758883640141232, 'flagsurrounded': -0.02395574694873867, 'yournumpieces': -0.01078281998170093, 'mynumpieces': 0.5385217847461586, 'distflagenemy': 1.0, 'mypiecesum': 0.5631366846940973, 'yoursumofpiecesrows': -0.03561273951110605}
        for key, value in newdict.iteritems():
            self.agents[1].weights[key] =value

        while not self.gameOver:
            turns += 1
            agent = self.agents[agentIndex]

           # print '\n'
           # print "AGENT", agent.index, "'s TURN"
           # print "--------------\n"

            action = agent.getAction(self.state)
            (piece, pos) = action
          #  print "ACTION:", (str(piece), piece.position, pos)

            nextState = self.state.getSuccessor(agentIndex, action)
           # agent.update(self.state, action, nextState)
            self.state = nextState

            #self.state.prnt(agent.index)

            if self.state.isWon(0):
                #print "Player 0 wins!"
                self.agent0wins += 1
                break
            if self.state.isWon(1):
                #print "Player 1 wins!"
                self.agent1wins += 1
                break
           # agent.final(self.state)

            agentIndex = 1-agentIndex
        #print "The game took", turns, "turns."

def main():
    agent0 = RandomAgent(0)
    agent1 = ApproximateQAgent(1, epsilon=0)
    #agent1 = RandomAgent(1)

    game = Game([agent0, agent1], 0)
    
    wi = agent1.weights.copy()
    for i in range(100):
        game.run()
        if (i%1 == 0):
            print "Weights after game", i, " are", agent1.weights
            print "Player 0 won", game.agent0wins, "times"
            print "Player 1 won", game.agent1wins, "times"
            print 
    print "Initial weights", wi
    print "Final weights", agent1.weights
    print "Player 0 won", game.agent0wins, "times"
    print "Player 1 won", game.agent1wins, "times"



if __name__ == "__main__": main()
