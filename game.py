from state import *
from Agent import *
from layout import getLayout
import time

BOARD = True
SCORE = True
WEIGHTS = False
SETUP = False
LEARN = False

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
            self.state.prnt()

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

            if BOARD:
                self.state.prnt(0)

            

            agentIndex = 1-agentIndex
            if BOARD: time.sleep(0.02)
        #print "The game took", turns, "turns."
        if LEARN:
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

    # weights after 5000 games, with fixed battle lookahead
    gameWeights = {'mysumofpiecesrows': 0.04625673695958664, 'yourpiecesum': -0.2570772693921104, 'numbombdiffusers': -0.32729497714886213, 'numbombs': 0.4430019701521672, 'flagsurrounded': -0.08653438783937016, 'yournumpieces': -0.25085262361947785, 'iwon': 0.0, 'mynumpieces': 0.8461602696655699, 'distflagenemy': 1.0, 'mypiecesum': 0.0436475151976312, 'yoursumofpiecesrows': -0.4661784801260383, 'youwon': 0.0}
    setupWeights = {'5x6': -1.065745277111735e-25, '5x7': -0.11133950891315199, '5x4': 9.38797466925448e-20, '5x5': 0.0010456782359999789, '5x2': -9.718274116447606e-30, '5x3': -1.1427867688340955e-21, '5x1': -8.919249901951485e-06, '5x8': -1.1451845425361168e-13, 'dist64': -0.5535963726625994, 'dist65': -0.22065009126385107, '3x2': 9.782353497986679e-16, '3x3': -0.11133950892344519, '3x4': 9.386848232923629e-20, 'dist61': -0.33302617532977624, 'dist62': -0.4443301074266898, 'dist63': -0.33305292725936525, '3x8': -1.0766316799952888e-25, '7x4': 9.43417481290433e-08, '7x5': 1.0182744231217881e-43, '7x6': -9.597647806661761e-10, '7x7': 0.0010366656144078746, '7x1': -1.1450917064233618e-13, '7x2': -9.190885578866422e-18, '7x3': -0.11133950892344519, '7x8': -9.717127099167785e-30, '9x8': 1.0293195630465342e-11, '8x3': -0.11029392502919336, '8x2': -1.931871753317504e-54, '8x1': -7.417339792339537e-46, '8x7': -9.70172485466141e-10, '8x6': 1.0293195630465342e-11, '8x5': 9.43417481290433e-08, '8x4': 1.0182744231217881e-43, '8x8': -8.918279843975192e-06, 'dist73': -0.11034725181480078, 'dist72': -0.44222992215532786, 'dist71': -0.7783753841862695, 'dist70': -0.11032030537107944, 'dist76': -0.44329353324397164, 'dist75': -0.6660171424797898, 'dist74': -0.5514961971121726, '3x1': -8.919249901951489e-06, '1x2': 9.434174812904328e-08, '1x3': -8.918279843975192e-06, '1x1': -9.284754168858825e-18, '1x6': 1.1265451948780412e-23, '1x7': 0.0010455838942518498, '1x4': 9.786310071531698e-32, '1x5': 1.029319572433382e-11, 'dist60': -0.33089933053206155, '1x8': -0.11133950989361768, '3x5': -1.1450916949955052e-13, '8y1': -0.11029392501890015, '8y2': -8.91827984298767e-06, '8y3': 9.337157464686501e-08, '3x6': 0.0010456782359989914, '0x3': -9.701714979460372e-10, '0x2': -8.943556151431856e-130, '0x1': -1.4060687504774802e-41, '3x7': 1.0293195630465342e-11, '0x7': -7.370790242238561e-46, '0x6': -8.823938096833668e-06, '0x5': -9.192017101271944e-18, '0x4': -0.11133950892344519, '4x8': -0.1113395089234452, '4x7': 1.0293195629322553e-11, 'dist87': -0.21851423772465967, 'dist84': -0.7783576467979186, 'dist85': -0.44333803223046764, 'dist82': -0.21955099671086922, 'dist83': -0.10827382626470877, 'dist80': -0.3288172726270197, 'dist81': -0.5515137477159703, '6x8': -8.91827995848436e-06, '0y1': 0.0010455839045460328, '6x5': -0.11133950892344519, '6x4': 9.434174714152317e-08, '6x7': -1.1427867688340955e-21, '6x6': 0.0010455839045460328, '6x1': -9.284754061205375e-18, '6x3': 9.386848232923629e-20, '6x2': -9.700579762966416e-10, '9x6': -1.1427867688340955e-21, '0y2': -9.70057976297773e-10, '0y3': -0.11134833286165655, 'dist98': -0.10826490699399245, 'dist95': -0.5514782623307336, 'dist94': -0.8886603909254401, 'dist97': -0.3267616836061942, 'dist96': -0.3288440245560362, 'dist91': -0.661781205770867, 'dist90': -0.4370286622226592, '4y2': 0.001036759956155016, 'dist92': -0.1072282423500976, '6y2': 0.0010456782462921871, '6y3': -8.91827984397519e-06, '6y1': -0.11133950989361668, 'dist10': -0.6659809985906266, '2x8': -8.919249901951489e-06, '2x1': -0.11133950892355969, '2x3': 9.901011665831528e-32, '2x2': 9.875201038598636e-16, '2x5': 0.0010455839045450455, '2x4': -9.190885578866422e-18, '2x7': 1.126544223165331e-23, '2x6': 9.434174714152317e-08, '0x8': 0.0010455839045450455, 'dist20': -0.5525507935974785, 'dist21': -0.7773384345766786, '4y1': -9.70056988682669e-10, 'dist93': -0.21643189290361836, '4y3': -0.11133950891326651, '2y2': 0.0010456782462931746, '2y3': -9.700579762966416e-10, '2y1': -0.11134842720340368, '4x3': 0.0010455838942518498, 'dist32': -0.33198969935897593, 'dist31': -0.6659722719145159, 'dist30': -0.22065009223413803, '9y1': -0.11133950892355872, '9y3': -8.919249901951392e-06, '9y2': 0.001045678246292187, 'dist86': -0.21850541864668688, '4x6': 1.0183206704094678e-43, '9x4': 1.0886402780315516e-27, '4x5': -8.823938096833572e-06, '4x4': 9.875201037522004e-16, 'dist42': -1.0, 'dist43': -0.6638991225996042, 'dist40': -0.4391021830839857, 'dist41': -0.218514148233314, '4x2': 9.901011664425459e-32, '4x1': -9.701724854661297e-10, '9x5': -9.61810666000008e-30, '5y1': -0.11029383068744522, '5y3': -8.91827995848436e-06, '5y2': -9.597647806673077e-10, '9x2': -0.11134842817334714, '9x3': 9.434174714152317e-08, '9x1': 0.00104558389425185, '1y1': -0.11133941555175601, '9x7': -1.1353093413848748e-13, '1y3': 1.0294183149426412e-11, '1y2': 0.0010366656142933562, '3y3': -9.700579762039045e-10, '3y2': -0.1113395089234452, '3y1': 0.0010367599663346902, '7y3': -0.11133950891315199, '7y2': -9.701714978521687e-10, '7y1': 0.001036759956155007, 'dist51': -0.10822923678467401, 'dist50': -0.553605103228549, 'dist53': -0.5556697039012493, 'dist52': -0.667071553222425, 'dist54': -0.3309262731056182}
    for key, value in gameWeights.iteritems():
        game.agents[0].weights[key] = value
    for key, value in setupWeights.iteritems():
        game.agents[0].setupWeights[key] = value

    wi = agent0.weights.copy()
    print "Initial weights", wi
    wis = agent0.setupWeights.copy()
    print "Initial setup weights", wis

    for i in range(5000):
        print
        print "--------------------"
        print "GAME", i
        game.run()
        if (i%1 == 0):
            if WEIGHTS:
                print "Agent 0 Weights after game", i, " are", agent0.weights
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
