from piece import *
from array2d import Array2d

WIDTH, HEIGHT = 8, 8

class Position:
    def __init__(self):
        self.pieces = []
        self.colormap = Array2d(WIDTH, HEIGHT)
        self.__legal_moves = []
        self.__legal_moves_cached = False
        self.to_move = Color.WHITE
    
    def __get_legal_moves(self):
        legal_moves = []
        return legal_moves

    @property
    def legal_moves(self):
        if not self.__legal_moves_cached:
            self.__legal_moves = self.__get_legal_moves()        
            self.__legal_moves_cached = True
        
        return self.__legal_moves     
    

    def is_legal(self, move):
        if move in self.legal_moves:
            return True
        
        return False
    
    def move(self, move: Move):
        pos1 = move.pos1
        pos2 = move.pos2
        for piece in self.pieces:
            if piece.pos == pos1:
                piece.move(pos2)
                self.colormap.set(pos2, self.colormap.at(pos1))
                self.colormap.set(pos1, Color.EMPTY)
                break

        for piece in self.pieces:
            if piece.pos == pos2:
                self.pieces.remove(piece)
                break    
        

