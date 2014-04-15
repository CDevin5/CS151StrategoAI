from util import Counter
import piece
import state

class FeatureExtractors:
    def getFeatures(self, state, agent):
        me = agent
        you = 1-agent

        flag = state.getFlag(me)
        feats = Counter()

        feats["mynumpieces"] = len(state.getAlivePieces(me))
        feats["yournumpieces"] = len(state.getAlivePieces(you))

        feats["mypiecesum"] = sum([p.rank for p in state.getAlivePieces(me)])
        feats["yourpiecesum"] = 52 - sum([11-p.rank for p in state.getDeadPieces(you)])

        feats["numbombdiffusers"] = sum([1 if p.rank == piece.MINER else 0 for p in state.getAlivePieces(me)])

        feats["numbombs"] = sum([1 if p.rank == piece.BOMB else 0 for p in state.getAlivePieces(me)])

        feats["distflagenemy"] = max([manhattanDistance(flag, p) for p in state.getAlivePieces(you)])

        feats["mysumofpiecesrows"] = sum([p.position[1] for p in state.getAlivePieces(me)])
        feats["yousumofpiecesrows"] = sum([p.position[1] for p in state.getAlivePieces(you)])

        flagx, flagy = flag.position
        surroundings = [(flagx, flagy+1), (flagx, flagy-1), (flagx-1, flagy), (flagx+1, flagy)]
        surrpieces = [state.getPieceAtPos(p) for p in surroundings]
        feats["flagsurrounded"] = sum([1 if (p != None and p.agentIndex == me) else 0 for p in surrpieces])

        # Maybe add the row of the general or the bomb diffusers

        return feats
    def getListOfFeatures(self):
        return ["mynumpieces", "yournumpieces", "mypiecesum", "yourpiecesum", "numbombdiffusers", "numbombs", 
                "distflagenemy", "mysumofpiecesrows", "yousumofpiecesrows", "flagsurrounded"]

def manhattanDistance(p1, p2):
    (x1,y1) = p1.position
    (x2,y2) = p2.position

    return abs(x2-x1) + abs(y2-y1)
