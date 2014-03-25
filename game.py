from gamestate import GameState, Agent

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
            action = agent.getAction(self.state)

            self.state = self.state.getSuccessor(agentIndex, action)
            self.state.show()

            if self.state.isWin:
                print "You Win!"
                return
            if self.state.isLose:
                print "You Lose"
                return

            agentIndex = 1-agentIndex

def main():
    agent0 = Agent()
    agent1 = Agent()
    game = Game([agent0, agent1], 1)

    game.run()

if __name__ == "__main__": main()