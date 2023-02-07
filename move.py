from enum import Enum

class MoveMeta(Enum):
    DEFAULT = "DEFAULT"
    CAPTURE = "CAPTURE"
    ENPASSANT = "ENPASSANT"
    PROMOTE = "PROMOTE"
    PROMOTE_CAPTURE = "PROMOTE_CAPTURE"
    SHORT_CASTLE = "SHORT_CASTLE"
    LONG_CASTLE = "LONG_CASTLE"

class Move:
    def __init__(self, pos1, pos2, meta):
        self.pos1 = pos1
        self.pos2 = pos2
        self.meta = meta

    def __repr__(self):
        return f"{self.pos1} -> {self.pos2} {self.meta.value}"