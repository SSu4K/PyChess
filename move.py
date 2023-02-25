from enum import Enum

class Flag(Enum):
    DEFAULT = ""
    CAPTURE = "x"
    CHECK = "+"
    MATE = "#"
    ENPASSANT = " e.p."
    PROMOTE = "="
    SHORT_CASTLE = "O-O"
    LONG_CASTLE = "O-O-O"
    
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

class Type(Enum):
    EMPTY = "Empty"
    PAWN = "Pawn"
    BISHOP = "Bishop"
    KNIGHT = "Knight"
    ROOK = "Rook"
    QUEEN = "Queen"
    KING = "King"

    @property
    def symbol(self):
        if self == Type.KNIGHT:
            return "N"
        return self.value[0]
    
    def __str__(self):
        return self.symbol

class Move:
    def __init__(self, type, pos1, pos2, flags):
        self.type = type
        self.pos1 = pos1
        self.pos2 = pos2
        self.flags = flags

    def __repr__(self):
        return f"{self.type} {self.pos1} -> {self.pos2} {self.flags}"
    
    def reversed(self):
        return Move(self.pos2, self.pos1, ())
