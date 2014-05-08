from state import *
from Agent import *
from layout import getLayout
import time

BOARD = False
SCORE = True
WEIGHTS = True
SETUP = False

TRAINING_GAMES = 2000
REAL_GAMES = 1000

class Game:
    def __init__(self, agents, startAgentIndex):
        self.agents = agents
        self.startAgentIndex = startAgentIndex

        self.agent0wins = 0
        self.agent1wins = 0

        self.num2000turns = 0

        self.learn = True


    def run(self):
        agentIndex = self.startAgentIndex

        agent0setup = self.agents[0].makeSetup()
        agent1setup = self.agents[1].makeSetup()

        self.state = GameState(getLayout("smallGrid.lay"),agent0setup, agent1setup)

        turns = 0

        if SETUP:
            self.state.prnt(0)

        while True:

            if self.state.isWon(0):
                self.agent0wins += 1
                break
            if self.state.isWon(1):
                self.agent1wins += 1
                break

            if turns > 2000:
                self.num2000turns += 1
                break

            turns += 1
            agent = self.agents[agentIndex]


            action = agent.getAction(self.state)

            nextState = self.state.getSuccessor(agentIndex, action)
            if self.learn:
                agent.update(self.state, action, nextState)
            self.state = nextState

            if BOARD:
                self.state.prnt(0)

            

            agentIndex = 1-agentIndex
            if BOARD: time.sleep(0.02)
        if self.learn:
            self.agents[0].final(self.state)
            self.agents[1].final(self.state)

        return turns

def main():
    agent0 = ApproximateQAgent(0, epsilon=0.5, alpha=0.2)
    agent1 = RandomAgent(1)

    game = Game([agent0, agent1], 0)


    print "--------------------"
    print "|  TRAINING GAMES  |"
    print "--------------------"
    game.learn = True
    runGameSet(game, agent0, TRAINING_GAMES, file("trainingOutput.txt", 'w'))

    game.learn = False
    agent0.exploreRate = 0
    agent1.exploreRate = 0

    game.agent0wins = 0
    game.agent1wins = 0
    game.num2000turns = 0

    print "\n"
    print "--------------------"
    print "|    REAL GAMES    |"
    print "--------------------"
    runGameSet(game, agent0, REAL_GAMES, file("realOutput.txt", 'w'))


def runGameSet(game, agent0, numGames, f):
    turns = 0

    for i in range(numGames):
        gameInfo =  "--------------------\n" + \
                    "       GAME %d\n"%i + \
                    "--------------------\n"
        f.write(gameInfo)
        print gameInfo

        turns += game.run()

        if (i%1 == 0):
            if WEIGHTS:
                print("Agent 0 Weights are %s\n"%agent0.weights)
            if SETUP:
                print("Agent 0 Setup Weights are %s\n"%agent0.setupWeights)
            scoreInfo =  "Player 0 won %d times\n"%game.agent0wins + \
                         "Player 1 won %d times\n"%game.agent1wins + \
                         "Num 2000 turns %d\n"%game.num2000turns
            f.write(scoreInfo)
            if SCORE:
                print scoreInfo
            f.write("\n")
            print
        if BOARD: time.sleep(5)

    finalStats =  "---------------------\n" + \
                  "     FINAL STATS\n" + \
                  "---------------------\n" + \
                  "Final setup weights: %s\n"%agent0.setupWeights + \
                  "Final weights: %s\n"%agent0.weights + \
                  "Player 0 won %d times\n"%game.agent0wins + \
                  "Player 1 won %d times\n"%game.agent1wins + \
                  "Num 2000 turns %d\n"%game.num2000turns + \
                  "Average game length: %d\n"%(turns/TRAINING_GAMES)

    f.write(finalStats)
    print finalStats

    f.close()


if __name__ == "__main__": main()
