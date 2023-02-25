from piece import *
from fen import FenFile
from move import Move, Flag, Type
from functools import cached_property

WIDTH, HEIGHT = 8, 8

class Position:
    def __init__(self):
        self.board = [[Empty((i, j), Color.EMPTY) for i in range(WIDTH)] for j in range(HEIGHT)]
        self.to_move = Color.WHITE
        self.__en_passant_square = (-1, -1)
        self.__kings_pos = {
            Color.WHITE: (-1, -1),
            Color.BLACK: (-1, -1)
        }
        self.__castle_rights = [False, False, False, False]
        self.__half_move_counter = 0
        self.move_counter = 0
    
    def __str__(self):
        out = ""
        for y in reversed(range(HEIGHT)):
            for x in range(WIDTH):
                out += self.board[x][y].__str__()
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
        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.board[x][y] = Empty((x, y), Color.EMPTY)
        
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

    @cached_property
    def pieces(self):
        pieces = []
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[x][y].__class__!=Empty:
                    pieces.append(self.board[x][y])
        return pieces            

    def attacked(self, color):
        attacked_list = []
        for piece in self.pieces:
            if piece.color == color:
                attacked_list += piece.attacked(self.board)
        return attacked_list

    def __is_attacked(self, x, y, color):
        if (x, y) in self.attacked(color):
            return True
        return False

    def __is_check(self):
        for piece in self.pieces:
            if piece.type == Type.KING and piece.color == self.to_move:
                x, y = piece.pos
                break
        return self.__is_attacked(x, y, self.to_move.opposite)

    @property
    def is_check(self):
        return self.__is_check()

    def get_suspected_moves(self, piece):
        moves = []
        type = piece.type
        if type == Type.PAWN:
            x, y = piece.pos
            if piece.advancement < 6:
                if self.board[x][y+piece.color].type == Type.EMPTY:
                    moves.append(Move(type, piece.pos, (x, y+piece.color), (Flag.DEFAULT,)))
                    if piece.advancement == 1 and self.board[x][y+2*piece.color].type == Type.EMPTY:
                        moves.append(Move(type, piece.pos, (x, y+2*piece.color), (Flag.DEFAULT,)))
            for square in piece.attacked(self.board):
                x, y = square
                if self.board[x][y].type != Type.EMPTY:
                    moves.append(Move(type, piece.pos, square, (Flag.CAPTURE,)))
                elif square == self.__en_passant_square:
                    moves.append(Move(type, piece.pos, square, (Flag.CAPTURE, Flag.ENPASSANT)))
        else:
            for square in piece.attacked(self.board):
                x, y = square
                if self.board[x][y].type != Type.EMPTY:
                    moves.append(Move(type, piece.pos, square, (Flag.CAPTURE,)))
                else:
                    moves.append(Move(type, piece.pos, square, (Flag.DEFAULT,)))
            
        return moves
    
    @cached_property
    def legal_moves(self):
        suspected_moves = []
        legal_moves = []
        for piece in self.pieces:
            if piece.color == self.to_move:
                suspected_moves += self.get_suspected_moves(piece)

        for move in suspected_moves:
            legal_moves.append(move)

        return legal_moves     
    


    @cached_property
    def legal_moves_dict(self):
        def file(x):
            letters = 'abcdefgh'
            return letters[x]

        def rank(y):
            numbers = '12345678'
            return numbers[y]

        def square(pos):
            return file(pos[0]) + rank(pos[1])

        move_dict = {}
        for move in self.legal_moves:
            type = move.type
            if type == Type.PAWN:
                if Flag.DEFAULT in move.flags:
                    move_dict[(square(move.pos2))] = move
                if Flag.CAPTURE in move.flags:
                    str = file(move.pos1[0])
                    str += Flag.CAPTURE.value
                    str += square(move.pos2)
                    if Flag.ENPASSANT in move.flags:
                        str += Flag.ENPASSANT.value
                    move_dict[str] = move
                continue
            
            str = move.type.symbol
            pos1 = move.pos1
            pos2 = move.pos2
            if not type == Type.KING:
                for move2 in self.legal_moves:
                    if move2 == move:
                        continue
                    if move2.type == type and move2.pos2 == pos2:
                        if pos1[1] == move.pos1[1]:
                            str += file(pos1[0])
                        if pos1[0] == move.pos1[0]:
                            str += rank(pos1[1])
                    if len(str) >= 3:
                        break
            if Flag.CAPTURE in move.flags:
                str += Flag.CAPTURE.value
            str += square(pos2)
            move_dict[str] = move
        return move_dict

    def is_legal(self, move):
        if move in self.legal_moves:
            return True
        
        return False
    
    def __move(self, move: Move):
        pos1 = move.pos1
        pos2 = move.pos2
        x1, y1 = pos1
        x2, y2 = pos2

        for piece in self.pieces:
            if piece.pos == pos2:
                self.pieces.remove(piece)
                break

        for piece in self.pieces:
            if piece.pos == pos1:
                piece.move(pos2)
                self.colormap[x2][y2] = self.colormap[x1][y1]
                self.colormap[x1][y1] = Color.EMPTY
                break 
    
    def move(self, move: Move):
        self.__move(move)
        if self.to_move == Color.WHITE:
            self.to_move = Color.BLACK
        else:
            self.to_move = Color.WHITE

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
                self.board[x][y] = Pawn((x, y), color)
            elif piece == "n":
                self.board[x][y] = Knight((x, y), color)
            elif piece == "b":
                self.board[x][y] = Bishop((x, y), color)
            elif piece == "r":
                self.board[x][y] = Rook((x, y), color)
            elif piece == "q":
                self.board[x][y] = Queen((x, y), color)
            elif piece == "k":
                self.board[x][y] = King((x, y), color)
                self.__kings_pos[color] = (x, y)
            
            x += 1

            


