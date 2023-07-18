import itertools
from functools import cached_property
from enum import IntEnum
from move import Type

class Color(IntEnum):
    WHITE = 1
    EMPTY = 0
    BLACK = -1
    def __repr__(self):
        return str(self.value)
    def __str__(self):
        return str(self.value)
    @property
    def opposite(self):
        return Color(-self.value)

def is_inside(x, y):
    if x<0: return 0
    if x>7: return 0
    if y<0: return 0
    if y>7: return 0
    return 1

class Piece:
    def __init__(self, pos, color):
        self.__pos = pos
        self.__color = color

    @property
    def type(self):
        return Type(self.__class__.__name__)

    def __repr__(self):
        out = ""
        out += self.type
        out += str(self.pos)

        return out

    def __str__(self):

        if self.color == Color.EMPTY:
            return "-"
        elif self.color == Color.WHITE:
            return self.type.value[0]
        else:
            return self.type.value.casefold()[0]

    @property
    def color(self):
        return self.__color
    
    @property
    def pos(self):
        return self.__pos
    
    @property
    def value(self):
        return 0

    def move(self, pos):
        self.__pos = pos

    def attacked(self, board):
        return []

class Empty(Piece):
    pass

class Pawn(Piece):

    @property
    def advancement(self):
        if self.color == Color.WHITE:
            home = 0
        else: home = 7
        return abs(home - self.pos[1])

    @property
    def value(self):
        return 1

    def attacked(self, board): 
        attacked_list = []
        x, y = self.pos
        color = self.color
        if x > 0:
            if board[x-1][y+color].color != color:
                attacked_list.append((x-1, y+color))
        if x < 7:
            if board[x+1][y+color].color != color:
                attacked_list.append((x+1, y+color))
        
        return attacked_list

class Knight(Piece):
    def __str__(self):
        if self.color == Color.WHITE:
            return "N"
        else:
            return "n"

    @property
    def value(self):
        return 3

    def attacked(self, board):
        attacked_list = []
        ones = (1, -1)
        twos = (2, -2)
        for m in itertools.product(ones, twos):
            x, y = self.pos
            x += m[0]
            y += m[1]
            if is_inside(x, y):
                if board[x][y].color != self.color:
                    attacked_list.append((x, y))
        for m in itertools.product(twos, ones):
            x, y = self.pos
            x += m[0]
            y += m[1]
            if is_inside(x, y):
                if board[x][y].color != self.color:
                    attacked_list.append((x, y))

        return attacked_list

class Bishop(Piece):

    @property
    def value(self):
        return 3

    def attacked(self, board):
        attacked_list = []
        for dx in (-1, 1):
            for dy in (-1, 1):
                x, y = self.pos
                x += dx
                y += dy
                while is_inside(x, y):
                    if board[x][y].color != self.color:
                        attacked_list.append((x, y))
                    if board[x][y].color != Color.EMPTY:
                        break
                    x += dx
                    y += dy
        return attacked_list


class Rook(Piece):

    @property
    def value(self):
        return 5

    def attacked(self, board):
        attacked_list = []
        for d in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            dx, dy = d
            x, y = self.pos
            x += dx
            y += dy
            while is_inside(x, y):
                if board[x][y].color != self.color:
                    attacked_list.append((x, y))
                if board[x][y].color != Color.EMPTY:
                    break
                x += dx
                y += dy
        return attacked_list

class Queen(Piece):

    @property
    def value(self):
        return 9

    def attacked(self, board):
        attacked_list = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                x, y = self.pos
                x += dx
                y += dy
                while is_inside(x, y):
                    if board[x][y].color != self.color:
                        attacked_list.append((x, y))
                    if board[x][y].color != Color.EMPTY:
                        break
                    x += dx
                    y += dy
        return attacked_list

class King(Piece):

    def attacked(self, board):
        attacked_list = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                x, y = self.pos
                x += dx
                y += dy
                if is_inside(x, y):
                    if board[x][y].color != self.color:
                        attacked_list.append((x, y))
        return attacked_list