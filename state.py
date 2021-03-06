from piece import *
import copy
import util

WALL      = '%'
EMPTY     = ' '
ENEMY     = '?'
MOVED     = 'M'
MOVED_FAR = 'X'

class GameState:
    def __init__(self, layout, agent0setup, agent1setup, agent0dead=[], agent1dead=[]):
        self.layout = layout

        self.player0pieces_alive = agent0setup
        self.player1pieces_alive = agent1setup

        self.player0pieces_dead = agent0dead
        self.player1pieces_dead = agent1dead

        width, height = self.layout.width, self.layout.height
        self.state = Grid(width, height)
        self.pieces = Grid(width, height)

        for x in range(width):
            for y in range(height):
                walls = self.layout.walls
                self.state[x][y] = self._wallStr(walls[x][y])
                self.pieces[x][y] = None

        for piece in self.player0pieces_alive:
            (x,y) = piece.position
            self.state[x][y] = str(piece)
            self.pieces[x][y] = piece

        for piece in self.player1pieces_alive:
            (x,y) = piece.position
            self.state[x][y] = str(piece)
            self.pieces[x][y] = piece

    @staticmethod
    def _wallStr(hasWall):
        if hasWall:
            return WALL
        else:
            return EMPTY

    def prnt(self, agent):
        print self.getState(agent)

    def getAlivePieces(self, agent):
        if agent == 0:
            return self.player0pieces_alive
        else:
            return self.player1pieces_alive

    def getDeadPieces(self, agent):
        if agent == 0:
            return self.player0pieces_dead
        else:
            return self.player1pieces_dead

    def getFlag(self, agent):

        for piece in self.getAlivePieces(agent):
            if piece.rank == FLAG:
                return piece

        return None

    def getPieceAtPos(self, position):
        x, y = position
        if not self.isInBounds(position):
            return None
        else:
            return self.pieces[x][y]

    def isFreeAtPos(self, position):
        x, y = position
        if self.pieces[x][y] is not None or self.state[x][y] == WALL:
            return False
        else:
            return True

    def isEnemyAtPos(self, position, agent):
        x, y = position
        if not self.isInBounds(position):
            return False
        piece = self.pieces[x][y]
        if piece is None:
            return False
        else:
            return piece.agentIndex != agent

    def isInBounds(self, position):
        x, y = position

        if x > 8 or x < 1 or y > 8 or y < 1:
            return False
        else:
            return True

    def getNeighborPositions(self, piece):
        x, y = piece.position
        neighbors = []

        if self.isInBounds((x + 1, y)):
            neighbors.append((x + 1, y))
        if self.isInBounds((x - 1, y)):
            neighbors.append((x - 1, y))
        if self.isInBounds((x, y + 1)):
            neighbors.append((x, y + 1))
        if self.isInBounds((x, y - 1)):
            neighbors.append((x, y - 1))

        return neighbors

    def copy(self):
        newplayer0pieces_alive = copy.deepcopy(self.player0pieces_alive)
        newplayer1pieces_alive = copy.deepcopy(self.player1pieces_alive)
        newplayer0pieces_dead = copy.deepcopy(self.player0pieces_dead)
        newplayer1pieces_dead = copy.deepcopy(self.player1pieces_dead)
        return GameState(self.layout, newplayer0pieces_alive, newplayer1pieces_alive, newplayer0pieces_dead,
                         newplayer1pieces_dead)

    def getState(self, agent):
        state = self.copy().state
        pieces = self.player1pieces_alive if agent == 0 else self.player0pieces_alive
        for piece in pieces:
            (x,y) = piece.position
            val = ENEMY
            # if piece.moved:
            #     val = MOVED
            state[x][y] = val
        return state

    def getSuccessor(self, agent, action):
        successor = self.copy()

        pieceIndex, newPos = action
        piece = successor.getAlivePieces(agent)[pieceIndex]
        oldx, oldy = piece.position
        x, y = newPos

        piece.moved = True
        if util.manhattanDistance(piece.position, newPos) > 1:
            piece.knownRank = True

        if successor.isEnemyAtPos(newPos, agent):
            enemy = successor.getPieceAtPos(newPos)
            result = piece.attack(enemy)

            if result == LOSE_FIGHT:
                successor.killPiece(piece, agent)
            if result == WIN_FIGHT or result == TAKE_FLAG:
                successor.killPiece(enemy, 1-agent)
                successor.state[x][y] = str(piece)
                successor.pieces[x][y] = piece
            if result == TIE_FIGHT:
                successor.killPiece(piece, agent)
                successor.killPiece(enemy, 1-agent)
            enemy.knownRank = enemy.rank
        else:
            successor.state[x][y] = str(piece)
            successor.pieces[x][y] = piece

        piece.position = newPos
        successor.state[oldx][oldy] = EMPTY
        successor.pieces[oldx][oldy] = None

        return successor

    def getSuccessorsProbs(self, agent, action):
        successor = self.copy()

        pieceIndex, newPos = action
        piece = successor.getAlivePieces(agent)[pieceIndex]
        oldx, oldy = piece.position
        x, y = newPos

        piece.moved = True

        successors = [(successor, 1.0)]

        if successor.isEnemyAtPos(newPos, agent):
            enemy = successor.getPieceAtPos(newPos)
            if enemy.knownRank is not None:
                result = piece.attack(enemy)
                if result == LOSE_FIGHT:
                    successor.killPiece(piece, agent)
                if result == WIN_FIGHT or result == TAKE_FLAG:
                    successor.killPiece(enemy, 1-agent)
                if result == TIE_FIGHT:
                    successor.killPiece(enemy, 1-agent)
                    successor.killPiece(piece, agent)

            else:
                enemies = successor.getAlivePieces(1-agent)
                numMoved = sum(1 if p.moved else 0 for p in enemies)
                numCanMove = sum(0 if p.rank == BOMB or p.rank == FLAG else 1 for p in enemies)
                if numCanMove == numMoved:
                    enemies = [e for e in enemies if e.rank == BOMB or e.rank == FLAG]

                numWins = 0
                numLosses = 0
                numTies = 0
                takeFlag = 0

                for e in enemies:
                    if not (enemy.moved and (e.rank == BOMB or e.rank == FLAG)):
                        result = piece.attack(e)

                        if result == LOSE_FIGHT:
                            numLosses += 1
                        if result == WIN_FIGHT:
                            numWins += 1
                        if result == TIE_FIGHT:
                            numTies += 1
                        if result == TAKE_FLAG:
                            takeFlag += 1

                successorWin = successor.copy()
                successorLose = successor.copy()
                successorTie = successor.copy()
                successorFlag = successor.copy()

                successorWin.killPiece(successorWin.getPieceAtPos(newPos), 1-agent)
                successorLose.killPiece(successorLose.getAlivePieces(agent)[pieceIndex], agent)
                successorTie.killPiece(successorTie.getPieceAtPos(newPos), 1-agent)
                successorTie.killPiece(successorTie.getAlivePieces(agent)[pieceIndex], agent)
                successorFlag.killPiece(successorFlag.getPieceAtPos(newPos), 1-agent)

                successorWin.state[x][y] = str(piece)
                successorWin.pieces[x][y] = piece

                total = float(numWins+numTies+numLosses+takeFlag)
                if total == 0: total = 1
                successors = [(successorWin, numWins/total), (successorLose, numLosses/total), (successorTie, numTies/total),
                              (successorFlag, takeFlag/total)]
        piece.position = newPos
        successor.state[oldx][oldy] = EMPTY
        successor.pieces[oldx][oldy] = None
        successor.state[x][y] = str(piece)
        successor.pieces[x][y] = piece

        return successors

    def killPiece(self, piece, agent):
        if agent == 0:
            self.player0pieces_dead.append(piece)
            self.player0pieces_alive.remove(piece)

            x, y = piece.position
            self.state[x][y] = EMPTY
            self.pieces[x][y] = None

        else:
            self.player1pieces_dead.append(piece)
            self.player1pieces_alive.remove(piece)

            x, y = piece.position
            self.state[x][y] = EMPTY
            self.pieces[x][y] = None

    def getLegalActions(self, agent):
        actions = []
        pieces = self.getAlivePieces(agent)
        for i in range(len(pieces)):
            piece = pieces[i]
            if piece.rank == SCOUT:
                x,y = piece.position
                scoutRanges = [range(x-1,-1,-1), range(x+1,self.layout.width), range(y-1,-1,-1), range(y+1, self.layout.height)]
                for j in range(4):
                    for xy in scoutRanges[j]:
                        if j <= 1:
                            pos = (xy,y)
                        else:
                            pos = (x,xy)
                        if self.isEnemyAtPos(pos, agent):
                            actions.append((i, pos))
                            break
                        if not self.isFreeAtPos(pos):
                            break
                        actions.append((i, pos))
            else:
                if piece.canMove:
                    neighborPos = self.getNeighborPositions(piece)

                    for pos in neighborPos:
                        if self.isFreeAtPos(pos) or self.isEnemyAtPos(pos, agent):
                            actions.append((i, pos))

        # print "Legal actions:", [(pieces[p].rank, pieces[p].position, pos) for (p,pos) in actions]
        return actions

    def isWon(self, agent):
        if agent == 0:
            if self.getFlag(1) is None:
                return True
            else:
                return self.getLegalActions(1) == []

        else:
            if self.getFlag(0) is None:
                return True
            else:
                return self.getLegalActions(0) == []


class Grid:
    """
    A 2-dimensional array of objects backed by a list of lists.  Data is accessed
    via grid[x][y] where (x,y) are positions on a Pacman map with x horizontal,
    y vertical and the origin (0,0) in the bottom left corner.

    The __str__ method constructs an output that is oriented like a pacman board.
    """

    def __init__(self, width, height, initialValue=False, bitRepresentation=None):
        if initialValue not in [False, True]: raise Exception('Grids can only contain booleans')
        self.CELLS_PER_INT = 30

        self.width = width
        self.height = height
        self.data = [[initialValue for _ in range(height)] for _ in range(width)]
        if bitRepresentation:
            self._unpackBits(bitRepresentation)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __str__(self):
        out = [[str(self.data[x][y])[0] for x in range(self.width)] for y in range(self.height)]
        out.reverse()

        cols = '\n  ' + ''.join([str(x) for x in range(self.width)])
        rows = range(self.height)
        rows.reverse()
        out = [[str(n),' '] + text for n,text in zip(rows,out)]

        return '\n'.join([''.join(x) for x in out]) + cols

    def __eq__(self, other):
        if other is None: return False
        return self.data == other.data

    def __hash__(self):
        # return hash(str(self))
        base = 1
        h = 0
        for l in self.data:
            for i in l:
                if i:
                    h += base
                base *= 2
        return hash(h)

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item=True):
        return sum([x.count(item) for x in self.data])

    def asList(self, key=True):
        l = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key: l.append((x, y))
        return l

    def packBits(self):
        """
        Returns an efficient int list representation

        (width, height, bitPackedInts...)
        """
        bits = [self.width, self.height]
        currentInt = 0
        for i in range(self.height * self.width):
            bit = self.CELLS_PER_INT - (i % self.CELLS_PER_INT) - 1
            x, y = self._cellIndexToPosition(i)
            if self[x][y]:
                currentInt += 2 ** bit
            if (i + 1) % self.CELLS_PER_INT == 0:
                bits.append(currentInt)
                currentInt = 0
        bits.append(currentInt)
        return tuple(bits)

    def _cellIndexToPosition(self, index):
        x = index / self.height
        y = index % self.height
        return x, y

    def _unpackBits(self, bits):
        """
        Fills in data from a bit-level representation
        """
        cell = 0
        for packed in bits:
            for bit in self._unpackInt(packed, self.CELLS_PER_INT):
                if cell == self.width * self.height: break
                x, y = self._cellIndexToPosition(cell)
                self[x][y] = bit
                cell += 1

    def _unpackInt(self, packed, size):
        bools = []
        if packed < 0: raise ValueError, "must be a positive integer"
        for i in range(size):
            n = 2 ** (self.CELLS_PER_INT - i - 1)
            if packed >= n:
                bools.append(True)
                packed -= n
            else:
                bools.append(False)
        return bools

