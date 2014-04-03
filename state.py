from piece import *


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
                self.walls = self.layout.walls
                self.state[x][y] = self._wallStr(self.walls[x][y])
                self.pieces[x][y] = None

        for piece in self.player0pieces_alive:
            (x,y) = piece.position
            self.state[x][y] = str(piece)
            self.pieces[x][y] = piece

        for piece in self.player1pieces_alive:
            (x,y) = piece.position
            self.state[x][y] = str(piece)
            self.pieces[x][y] = piece

    def _wallStr(self, hasWall):
        if hasWall:
            return '%'
        else:
            return ' '

    def __str__(self):
        return str(self.state)

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
        if self.pieces[x][y] == None:
            return True
        else:
            return False

    def isEnemyAtPos(self, position, agent):
        x, y = position
        piece = self.pieces[x][y]
        if piece == None:
            return False
        else:
            return piece.agentIndex != agent

    def isInBounds(self, position):
        x, y = position

        if x > 7 or x < 0 or y > 7 or y < 0:
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
        return GameState(self.layout, self.player0pieces_alive, self.player1pieces_alive, self.player0pieces_dead,
                         self.player1pieces_dead)

    def getState(self, agent):
        return self.state

    def getSuccessor(self, agent, action):
        successor = self.copy()

        piece, newPos = action
        oldx, oldy = piece.position
        x, y = newPos

        if successor.isEnemyAtPos(newPos, agent):
            enemy = self.getPieceAtPos(newPos)
            result = piece.attack(enemy)

            if result == LOSE_FIGHT:
                successor.killPiece(piece, agent)
            if result == WIN_FIGHT:
                successor.killPiece(enemy, 1-agent)
            if result == TIE_FIGHT:
                successor.killPiece(piece, agent)
                successor.killPiece(enemy, 1-agent)

        piece.position = newPos
        successor.state[oldx][oldy] = successor._wallStr(self.walls[oldx][oldy])
        successor.pieces[oldx][oldy] = None

        successor.state[x][y] = str(piece)
        successor.pieces[x][y] = piece

        return successor

    def killPiece(self, piece, agent):
        if agent == 0:
            self.player0pieces_dead.append(piece)
            self.player0pieces_alive.remove(piece)

            x, y = piece.position
            self.state[x][y] = self._wallStr(self.walls[x][y])
            self.pieces[x][y] = None

        else:
            self.player1pieces_dead.append(piece)
            self.player1pieces_alive.remove(piece)

            x, y = piece.position
            self.state[x][y] = self._wallStr(self.walls[x][y])
            self.pieces[x][y] = None

    def getLegalActions(self, agent):
        actions = []

        for piece in self.getAlivePieces(agent):
            if piece.canMove:
                neighborPos = self.getNeighborPositions(piece)

                for pos in neighborPos:
                    if self.isFreeAtPos(pos) or self.isEnemyAtPos(pos, agent):
                        actions.append((piece, pos))

        return actions

    def isWon(self, agent):
        if agent == 0:
            if self.getFlag(1) == None:
                return True
            else:
                return self.getLegalActions(1) == []

        else:
            if self.getFlag(0) == None:
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
        self.data = [[initialValue for y in range(height)] for x in range(width)]
        if bitRepresentation:
            self._unpackBits(bitRepresentation)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __str__(self):
        out = [[str(self.data[x][y])[0] for x in range(self.width)] for y in range(self.height)]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])

    def __eq__(self, other):
        if other == None: return False
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
        list = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key: list.append((x, y))
        return list

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
