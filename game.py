from state import *
from Agent import *
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

        while not self.gameOver:
            agent = self.agents[agentIndex]
            print '\n'
            print "AGENT", agent.index, "'s TURN"
            print "--------------\n"

            action = agent.getAction(self.state)
            (piece, pos) = action
            print "ACTION:", (str(piece), piece.position, pos)

            self.state = self.state.getSuccessor(agentIndex, action)
            print self.state

            if self.state.isWon(0):
                print "Player 0 wins!"
                return
            if self.state.isWon(1):
                print "Player 1 wins!"
                return

            agentIndex = 1-agentIndex

def main():
    agent0 = RandomAgent(0)
    agent1 = HumanAgent(1)
    game = Game([agent0, agent1], 0)

    game.run()

if __name__ == "__main__": main()
