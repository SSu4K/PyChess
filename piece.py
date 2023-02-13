import itertools
from enum import IntEnum
from move import Move, Flag

class Color(IntEnum):
    WHITE = 1
    EMPTY = 0
    BLACK = -1
    def __repr__(self):
        return str(self.value)
    def __str__(self):
        return str(self.value)

def is_inside(x, y):
    if x<0: return 0
    if x>7: return 0
    if y<0: return 0
    if y>7: return 0
    return 1

class Piece:
    def __init__(self, pos, color):
        self._pos = pos
        self._color = color

    def __repr__(self):
        out = ""
        out += self.__class__.__name__
        out += str(self.pos)

        return out

    def __str__(self):
        if self.color == Color.WHITE:
            return self.__class__.__name__[0]
        else:
            return self.__class__.__name__.casefold()[0]

    @property
    def color(self):
        return self._color
    
    @property
    def pos(self):
        return self._pos

    def move(self, pos):
        self._pos = pos

    def get_moves(self):
        pass

class Pawn(Piece):

    @property
    def advancement(self):
        if self.color == Color.WHITE:
            home = 0
        else: home = 7
        return abs(home - self.pos[1])

    def __get_captures(self, flags):
        move_list = []
        x, y = self.pos
        if(y>0):
            move_list.append(Move(self.pos, (x-1, y+self.color), flags))
        if(y<7):
            move_list.append(Move(self.pos, (x+1, y+self.color), flags))

        return move_list 

    def get_moves(self): 
        move_list = []
        x, y = self.pos
        if self.advancement < 6:
            move_list.append(Move(self.pos, (x, y+self.color), ()))
            move_list += self.__get_captures(Flag.CAPTURE)
        else:
            move_list.append(Move(self.pos, (x, y+self.color), (Flag.PROMOTE)))
            move_list += self.__get_captures((Flag.PROMOTE, Flag.CAPTURE))
        if self.advancement == 4:
            move_list += self.__get_captures((Flag.ENPASSANT, Flag.CAPTURE))

        return move_list

class Knight(Piece):
    def __str__(self):
        if self.color == Color.WHITE:
            return "N"
        else:
            return "n"

    def __add_move(self, move, flags, list):
        x, y = self.pos
        a, b = move
        x += a
        y += b
        if is_inside(x, y):
            list.append(Move(self.pos, (x, y), flags))
    

    def get_moves(self):
        move_list = []
        ones = (1, -1)
        twos = (2, -2)

        for m in itertools.product(ones, twos):
            self.__add_move(m, (Flag.CAPTURE,), move_list)
            self.__add_move(m, (), move_list)
        for m in itertools.product(twos, ones):
            self.__add_move(m, (Flag.CAPTURE,), move_list)
            self.__add_move(m, (), move_list)

        return move_list

class Bishop(Piece):
    pass

class Rook(Piece):
    pass

class Queen(Piece):
    pass

class King(Piece):
    pass