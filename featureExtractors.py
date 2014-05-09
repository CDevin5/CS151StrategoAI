from util import Counter
import piece
import state

class FeatureExtractors:
    def getFeatures(self, state, agent):
        me = agent
        you = 1-agent

        flag = state.getFlag(me)
        feats = Counter()

        myAlive = state.getAlivePieces(me)
        yourAlive = state.getAlivePieces(you)

        feats["mynumpieces"] = len(myAlive)/10.0
        feats["yournumpieces"] = len(yourAlive)/10.0

        feats["mypiecesum"] = sum([p.rank for p in myAlive])/52.0
        feats["yourpiecesum"] = sum([p.rank for p in yourAlive])/52.0

        feats["numbombdiffusers"] = sum([1 if p.rank == piece.MINER else 0 for p in myAlive])/3.0

        feats["numbombs"] = sum([1 if p.rank == piece.BOMB else 0 for p in myAlive])/3.0

        feats["distflagenemy"] = float("inf") if len(yourAlive) == 0 else min([manhattanDistance(flag, p) for p in yourAlive])/15.0

        feats["mysumofpiecesrows"] = sum([p.position[1] for p in myAlive])/80.0
        feats["yoursumofpiecesrows"] = sum([p.position[1] for p in yourAlive])/80.0

        flagx, flagy = flag.position
        surroundings = [(flagx, flagy+1), (flagx, flagy-1), (flagx-1, flagy), (flagx+1, flagy)]
        surrpieces = [state.getPieceAtPos(p) for p in surroundings]
        feats["flagsurrounded"] = sum([1 if (p != None and p.agentIndex == me) else 0 for p in surrpieces])/4.0

        # Maybe add the row of the general or the bomb diffusers

        return feats
    def getListOfFeatures(self):
        return ["mynumpieces", "yournumpieces", "mypiecesum", "yourpiecesum", "numbombdiffusers", "numbombs", 
                "distflagenemy", "mysumofpiecesrows", "yousumofpiecesrows", "flagsurrounded"]

class SetupFeatures:
    def getFeatures(self, pieces):
        feats = Counter()

        for i in range(len(pieces)):
            p = pieces[i]
            feats[str(i) + "x" + str(p.position[0])] =1
            feats[str(i) + "y" + str(p.position[1])] =1
            
            for j in range(i):
                feats["dist"+str(i)+str(j)] = manhattanDistance(p, pieces[j])

        return feats


def manhattanDistance(p1, p2):
    (x1,y1) = p1.position
    (x2,y2) = p2.position

    return abs(x2-x1) + abs(y2-y1)
