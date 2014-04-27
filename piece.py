# A Stratego piece is represented as a tuple (rank, position, color), 
# where rank is a character, position is a tuple (x,y) of the piece's 
# position on the board, 

# Piece names
MARSHALL   = 1
GENERAL    = 2
COLONEL    = 3
MAJOR      = 4
CAPTAIN    = 5
LIEUTENANT = 6
SERGEANT   = 7
MINER      = 8
SCOUT      = 9
SPY        = 10
BOMB       = 0
FLAG       = 11

# Fight outcomes
WIN_FIGHT  = 1
LOSE_FIGHT = 0
TIE_FIGHT  = 2
TAKE_FLAG  = 3

class Piece:

    def __init__(self, rank, position, agentIndex):
        self.rank = rank
        self.position = position
        self.agentIndex = agentIndex

        self.moved = False
        self.knownRank = None

        self.canMove = True

        if rank == BOMB or rank == FLAG:
            self.canMove = False

    def __str__(self):
        if self.rank > 0 and self.rank < 10:
            return str(self.rank)
        elif self.rank == BOMB:
            return 'B'
        elif self.rank == SPY:
            return 'S'
        elif self.rank == FLAG:
            return 'F'
        else:
            return '?'

    def attack(self, otherPiece):
        if self.canMove:
            if otherPiece.rank == FLAG:
                return TAKE_FLAG
            elif self.rank == SPY and otherPiece.rank == MARSHALL:
                return WIN_FIGHT
            elif self.rank == MARSHALL and otherPiece.rank == SPY:
                return LOSE_FIGHT
            elif self.rank == MINER and otherPiece.rank == BOMB:
                return WIN_FIGHT
            elif self.rank == BOMB and otherPiece.rank == MINER:
                return LOSE_FIGHT
            else:
                if self.rank < otherPiece.rank:
                    return WIN_FIGHT
                elif self.rank > otherPiece.rank:
                    return LOSE_FIGHT
                else:
                    return TIE_FIGHT

