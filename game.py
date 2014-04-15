from state import *
from Agent import *
from qlearningAgents import *
from layout import getLayout

class Game:
    def __init__(self, agents, startAgentIndex):
        self.agents = agents
        self.startAgentIndex = startAgentIndex

        self.gameOver = False

    def run(self):
        agentIndex = self.startAgentIndex

        agent0setup = self.agents[0].makeSetup()
        agent1setup = self.agents[1].makeSetup()

        self.state = GameState(getLayout("smallGrid.lay"),agent0setup, agent1setup)

        turns = 0

        while not self.gameOver:
            turns += 1
            agent = self.agents[agentIndex]
            print '\n'
            print "AGENT", agent.index, "'s TURN"
            print "--------------\n"

            action = agent.getAction(self.state)
            (piece, pos) = action
            print "ACTION:", (str(piece), piece.position, pos)

            self.state = self.state.getSuccessor(agentIndex, action)
            self.state.prnt(agent.index)

            if self.state.isWon(0):
                print "Player 0 wins!"
                break
            if self.state.isWon(1):
                print "Player 1 wins!"
                break
            agent.final(self.state)

            agentIndex = 1-agentIndex
        print "The game took", turns, "turns."

def main():
    agent0 = RandomAgent(0)
    agent1 = ApproximateQAgent(1)
    #agent1 = RandomAgent(1)
    game = Game([agent0, agent1], 0)
    agent1.startEpisode()
    game.run()

if __name__ == "__main__": main()
