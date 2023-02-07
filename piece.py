from enum import IntEnum
from move import Move, MoveMeta

class Color(IntEnum):
    WHITE = 1
    BLACK = -1

class Piece:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def move(self, pos):
        self.pos = pos

    def get_moves(self):
        pass

class Pawn(Piece):

    @property
    def advancement(self):
        if self.color == Color.WHITE:
            home = 0
        else: home = 7
        return abs(home - self.pos[1])

    def __get_captures(self, meta):
        move_list = []
        x, y = self.pos
        if(y>0):
            move_list.append(Move(self.pos, (x-1, y+self.color), meta))
        if(y<7):
            move_list.append(Move(self.pos, (x+1, y+self.color), meta))

        return move_list 

    def get_moves(self): 
        move_list = []
        x, y = self.pos
        if self.advancement < 6:
            move_list.append(Move(self.pos, (x, y+self.color), MoveMeta.DEFAULT))
            move_list += self.__get_captures(MoveMeta.CAPTURE)
        else:
            move_list.append(Move(self.pos, (x, y+self.color), MoveMeta.PROMOTE))
            move_list += self.__get_captures(MoveMeta.PROMOTE_CAPTURE)
        if self.advancement == 4:
            move_list += self.__get_captures(MoveMeta.ENPASSANT)

        return move_list

