from piece import *
from fen import FenFile
from move import Move, Flag, Type
from functools import cached_property
from copy import deepcopy, copy

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
        self.__castle_rights = {
            (Color.WHITE, Flag.LONG_CASTLE): False,
            (Color.WHITE, Flag.SHORT_CASTLE): False,
            (Color.BLACK, Flag.LONG_CASTLE): False,
            (Color.BLACK, Flag.SHORT_CASTLE): False
        }
        self.__half_move_counter = 0
        self.move_counter = 0
    
    def str_board(self):
        out = " ________________\n|"
        for y in reversed(range(HEIGHT)):
            for x in range(WIDTH):
                out += self.board[x][y].__str__()
                out += " "
            out += f"| {y+1}\n|"
        out += "________________|\n"
        out += " A B C D E F G H\n"
        return out

    def __str__(self):
        out = ""
        out += self.str_board()

        out += "\nTo move: " + str(self.to_move.name)
        out += "\nWhite short castle: " + str(self.__castle_rights[(Color.WHITE, Flag.SHORT_CASTLE)])
        out += "\nWhite long castle: " + str(self.__castle_rights[(Color.WHITE, Flag.LONG_CASTLE)])
        out += "\nBlack short castle: " + str(self.__castle_rights[(Color.BLACK, Flag.SHORT_CASTLE)])
        out += "\nBlack long castle: " + str(self.__castle_rights[(Color.BLACK, Flag.LONG_CASTLE)])
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

    @property
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

    def __is_attacked(self, pos, color):
        if pos in self.attacked(color):
            return True
        return False

    def __is_check(self):
        
        return self.__is_attacked(self.__kings_pos[self.to_move], self.to_move.opposite)

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
                if self.board[x][y].color == piece.color.opposite:
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
    
    @property
    def legal_moves(self):
        suspected_moves = []
        legal_moves = []
        for piece in self.pieces:
            if piece.color == self.to_move:
                suspected_moves += self.get_suspected_moves(piece)

        for move in suspected_moves:
            x2, y2 = move.pos2
            if Flag.ENPASSANT in move.flags:
                y2 -= self.to_move
                piece = deepcopy(self.board[x2][y2])
                self.board[x2][y2] = Empty((), Color.EMPTY)
            else:
                piece = deepcopy(self.board[x2][y2])
            self.__move(move)
            if not self.__is_check():    
                legal_moves.append(move)
            self.__move(move.reversed())
            self.board[x2][y2] = piece
        
        attacked = self.attacked(self.to_move.opposite)
        if self.__castle_rights[(self.to_move, Flag.SHORT_CASTLE)] and not self.is_check:
            legal = True
            if self.to_move == Color.WHITE:
                for x in range(5, 7):
                    if (x, 0) in attacked or (self.board[x][0].color != Color.EMPTY):
                        legal = False
                        break
                if legal:
                    legal_moves.append(Move(Type.KING, (4,0), (6,0), (Flag.SHORT_CASTLE,)))
            if self.to_move == Color.BLACK:
                for x in range(5, 7):
                    if (x, 7) in attacked or (self.board[x][7].color != Color.EMPTY):
                        legal = False
                        break
                if legal:
                    legal_moves.append(Move(Type.KING, (4,7), (6,7), (Flag.SHORT_CASTLE,)))
        if self.__castle_rights[(self.to_move, Flag.LONG_CASTLE)] and not self.is_check:
            legal = True
            if self.to_move == Color.WHITE:
                for x in range(2, 4):
                    if (x, 0) in attacked or (self.board[x][0].color != Color.EMPTY):
                        legal = False
                        break
                if legal:
                    legal_moves.append(Move(Type.KING, (4,0), (2,0), (Flag.LONG_CASTLE,)))
            if self.to_move == Color.BLACK:
                for x in range(2, 4):
                    if (x, 7) in attacked or (self.board[x][7].color != Color.EMPTY):
                        legal = False
                        break
                if legal:
                    legal_moves.append(Move(Type.KING, (4,7), (2,7), (Flag.LONG_CASTLE,)))
        
        return legal_moves     
    
    @property
    def legal_moves_dict(self):
        def file(pos):
            letters = 'abcdefgh'
            return letters[pos[0]]

        def rank(pos):
            numbers = '12345678'
            return numbers[pos[1]]

        def square(pos):
            return file(pos) + rank(pos)

        move_dict = {}
        for move in self.legal_moves:
            str = ""
            type = move.type
            pos1 = move.pos1
            pos2 = move.pos2
            specify_x = False
            specify_y = False
            if Flag.LONG_CASTLE in move.flags:
                move_dict[Flag.LONG_CASTLE.value] = move
                continue
            if Flag.SHORT_CASTLE in move.flags:
                move_dict[Flag.SHORT_CASTLE.value] = move
                continue
            if type == Type.PAWN:
                if Flag.CAPTURE in move.flags:
                    str = file(move.pos1)
            elif not type == Type.KING:
                str = move.type.symbol
                for move2 in self.legal_moves:
                    if move2.pos1 == pos1 or move2.type != type:
                        continue

                    if move2.pos2 == pos2:
                        if pos1[0] == move2.pos1[0]:
                            specify_y = True
                        else:
                            specify_x = True
                    if specify_x and specify_y:
                        break
            else:
                str = move.type.symbol
            if specify_x:
                str += file(pos1)
            if specify_y:
                str += rank(pos1)
            if Flag.CAPTURE in move.flags:
                str += Flag.CAPTURE.value
            str += square(pos2)

            if Flag.ENPASSANT in move.flags:
                str += Flag.ENPASSANT.value

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

        if move.type == Type.KING:
            self.__kings_pos[self.to_move] = pos2

        if Flag.SHORT_CASTLE in move.flags:
            self.board[7][y1] = Empty((7, y1), Color.EMPTY)
            self.board[5][y1] = Rook((5, y1), self.to_move)

        if Flag.LONG_CASTLE in move.flags:
            self.board[0][y1] = Empty((7, y1), Color.EMPTY)
            self.board[3][y1] = Rook((3, y1), self.to_move)

        self.board[x2][y2] = copy(self.board[x1][y1])
        self.board[x1][y1] = Empty((x1, y1), Color.EMPTY)
        self.board[x2][y2].move((x2, y2))
    
    def move(self, move: Move):
        self.__move(move)
        self.__en_passant_square = (-1, -1)
        if move.type == Type.PAWN:
            if abs(move.pos2[1] - move.pos1[1]) == 2:
                self.__en_passant_square = (move.pos2[0], move.pos2[1] - self.to_move)
        
        if Flag.ENPASSANT in move.flags:
            self.board[move.pos2[0]][move.pos2[1]-self.to_move] = Empty((), Color.EMPTY)

        if move.type == Type.KING:
            self.__castle_rights[(self.to_move, Flag.SHORT_CASTLE)] = False
            self.__castle_rights[(self.to_move, Flag.LONG_CASTLE)] = False

        if move.type == Type.ROOK:
            if self.to_move == Color.WHITE:
                if move.pos1 == (0, 0):
                    self.__castle_rights[(Color.WHITE, Flag.SHORT_CASTLE)] = False
                if move.pos1 == (0, 7):
                    self.__castle_rights[(Color.WHITE, Flag.LONG_CASTLE)] = False
            else:
                if move.pos1 == (7, 0):
                    self.__castle_rights[(Color.BLACK, Flag.SHORT_CASTLE)] = False
                if move.pos1 == (7, 7):
                    self.__castle_rights[(Color.BLACK, Flag.LONG_CASTLE)] = False

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

            


