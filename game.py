from state import *
from Agent import *

class Game:
    def __init__(self, agents, startAgentIndex):
        self.agents = agents
        self.startAgentIndex = startAgentIndex

        self.gameOver = False

    def run(self):
        agentIndex = self.startAgentIndex

        agent0setup = self.agents[0].setUpBoard()
        agent1setup = self.agents[1].setUpBoard()

        self.state = GameState(agent0setup, agent1setup)

        while not self.gameOver:
            agent = self.agents[agentIndex]
            print "AGENT " + agent + "'s TURN"
            print "--------------\n"

            action = agent.getAction(self.state)
            print "ACTION:", action

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
    agent0 = Agent(0)
    agent1 = Agent(1)
    game = Game([agent0, agent1], 1)

    game.run()

if __name__ == "__main__": main()
