# A Stratego piece is represented as a tuple (rank, position, color), 
# where rank is a character, position is a tuple (x,y) of the piece's 
# position on the board, 

# Piece names
MARSHALL   = 10
GENERAL    = 9
COLONEL    = 8
MAJOR      = 7
CAPTAIN    = 6
LIEUTENANT = 5
SERGEANT   = 4
MINER      = 3
SCOUT      = 2
SPY        = 1
BOMB       = 11
FLAG       = 0

# Fight outcomes
WIN_FIGHT  = 1
LOSE_FIGHT = 0
TIE_FIGHT  = 2
TAKE_FLAG  = 3

class Piece:

    def __init__(self, rank, position, color):
        self.rank = rank
        self.position = position
        self.color = color

        self.canMove = True

        if rank == BOMB or rank == FLAG:
            self.canMove = False

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
                if self.rank > otherPiece.rank:
                    return WIN_FIGHT
                elif self.rank < otherPiece.rank:
                    return LOSE_FIGHT
                else:
                    return TIE_FIGHT

