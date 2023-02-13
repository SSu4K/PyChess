from piece import Color

def is_01(num):
    if num == 0 or num == 1:
        return 1
    return 0

class FenFile:
    def __init__(self):
        self.active = Color.WHITE
        self.pieces = ""
        self.en_passant_square = (-1, -1)
        self.castle_rights = [True, True, True, True]
        self.half_move_counter = 0
        self.move_counter = 0
        self.good = False

    def __str__(self):
        return str(self.pieces)+str(self.active)

    def check_string(self, fen):
        pieces, active, castling, ep, hc, mc = fen.split()
        legal = "KQRBNPkqrbnp/123456789"
        for i in pieces:
            if legal.find(i) == -1:
                return 0
        if active != "w" and active != "b":
            return 0
        K = castling.count("K")
        Q = castling.count("Q")
        k = castling.count("k")
        q = castling.count("q")

        if not(is_01(K) and is_01(Q) and is_01(k) and is_01(q)):
            return 0
        if K+Q+k+q == 0 and castling != "-":
            return 0
        
        if ep != '-':
            if len(ep) != 2:
                return 0
            if ord(ep[0]) < 97 or ord(ep[0]) > 104:
                return 0
            if ord(ep[1]) < 49 or ord(ep[1]) > 57:
                return 0
        
        if (len(hc) != 1 or not hc.isdecimal()) and hc != '-':
            return 0
        if (len(mc) != 1 or not mc.isdecimal()) and mc != '-':
            return 0
        
        return 1

    def from_string(self, fen):
        if not self.check_string(fen):
            return
        
        pieces, active, castling, ep, hc, mc = fen.split()
        self.is_good = True
        self.pieces = pieces
        
        if active == "w":
            self.active = Color.WHITE
        else:
            self.active = Color.BLACK
        
        self.castle_rights[0] = castling.count("K")
        self.castle_rights[1] = castling.count("Q")
        self.castle_rights[2] = castling.count("k")
        self.castle_rights[3] = castling.count("q")

        if ep != "-":
            self.en_passant_square = (ord(ep[0])-97, ord(ep[1])-49)

        self.half_move_counter = int(hc[0])
        self.move_counter = int(mc[0])
        
