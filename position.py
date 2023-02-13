from piece import *
from array2d import Array2d
from fen import FenFile

WIDTH, HEIGHT = 8, 8

class Position:
    def __init__(self):
        self.pieces = []
        self.colormap = arr = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]
        self.__legal_moves = []
        self.__legal_moves_cached = False
        self.to_move = Color.WHITE
        self.__en_passant_square = (-1, -1)
        self.__castle_rights = [False, False, False, False]
        self.__half_move_counter = 0
        self.move_counter = 0
    
    def __str__(self):
        out = ""
        for y in reversed(range(HEIGHT)):
            for x in range(WIDTH):
                if self.colormap[x][y] != Color.EMPTY:
                    for piece in self.pieces:
                        if piece.pos == (x, y):
                            out += piece.__str__()
                            break
                else:
                    out += "-"
                out += " "
            out += "\n"

        out += "\nTo move: " + str(self.to_move.name)
        out += "\nWhite short castle: " + str(self.__castle_right(Color.WHITE, Flag.SHORT_CASTLE))
        out += "\nWhite long castle: " + str(self.__castle_right(Color.WHITE, Flag.LONG_CASTLE))
        out += "\nBlack short castle: " + str(self.__castle_right(Color.BLACK, Flag.SHORT_CASTLE))
        out += "\nBlack long castle: " + str(self.__castle_right(Color.BLACK, Flag.LONG_CASTLE))
        out += "\nEn-passant square: " + str(self.__en_passant_square)
        out += "\nHalf-move count: " + str(self.__half_move_counter)
        out += "\nMove count: " + str(self.move_counter)

        return out

    def clear(self):
        self.pieces.clear()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.colormap[x][y] = Color.EMPTY
        
        self.__legal_moves.clear()
        self.__legal_moves_cached = False
        self.to_move = Color.WHITE
        self.__en_passant_square = (-1, -1)
        self.__castle_rights = [False, False, False, False]
        self.__half_move_counter = 0
        self.move_counter = 0

    def __castle_right(self, color, flag):
        if color == Color.EMPTY:
            return 0
        if flag == Flag.LONG_CASTLE:
            return self.__castle_rights[1-color]
        elif flag == Flag.SHORT_CASTLE:
            return self.__castle_rights[1-color+1]
        return 0

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
        x1, y1 = pos1
        x2, y2 = pos2
        for piece in self.pieces:
            if piece.pos == pos1:
                piece.move(pos2)
                self.colormap[x2][y2] = self.colormap[x1][y1]
                self.colormap[x1][y1] = Color.EMPTY
                break

        for piece in self.pieces:
            if piece.pos == pos2:
                self.pieces.remove(piece)
                break    
    
    def load(self, fen: FenFile):
        self.clear()

        self.to_move = fen.active
        self.__castle_rights = fen.castle_rights
        self.__en_passant_square = fen.en_passant_square
        self.__half_move_counter = fen.half_move_counter
        self.move_counter = fen.move_counter

        x = 0
        y = 7

        for i in fen.pieces:
            if i == '/':
                y -= 1
                x = 0
                continue
            
            if i.isnumeric():
                x += int(i)
                continue

            if i.islower():
                color = Color.BLACK
            else:
                color = Color.WHITE
            
            piece = i.casefold()

            if piece == "p":
                self.pieces.append(Pawn((x, y), color))
            elif piece == "n":
                self.pieces.append(Knight((x, y), color))
            elif piece == "b":
                self.pieces.append(Bishop((x, y), color))
            elif piece == "r":
                self.pieces.append(Rook((x, y), color))
            elif piece == "q":
                self.pieces.append(Queen((x, y), color))
            elif piece == "k":
                self.pieces.append(King((x, y), color))
            
            x += 1

        for piece in self.pieces:
            self.colormap[piece.pos[0]][piece.pos[1]] = piece.color

            


