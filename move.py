from enum import Enum

class Flag(Enum):
    CAPTURE = "CAPTURE"
    ENPASSANT = "ENPASSANT"
    PROMOTE = "PROMOTE"
    SHORT_CASTLE = "SHORT_CASTLE"
    LONG_CASTLE = "LONG_CASTLE"
    
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

class Move:
    def __init__(self, pos1, pos2, flags):
        self.pos1 = pos1
        self.pos2 = pos2
        self.flags = flags

    def __repr__(self):
        return f"{self.pos1} -> {self.pos2} {self.flags}"