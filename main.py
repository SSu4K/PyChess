from position import Position, Move, Color
from fen import FenFile


fen = FenFile()
position = Position()

#fen.from_string("rnbqkbnr/pp2pppp/2p5/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 2")
#fen.from_string("2k5/8/8/1Ppp1p2/4P1p1/1P3P2/3P2P1/2K5 w - c6 0 1")
fen.from_string("8/8/B7/5p2/8/1r1QK3/8/1R1p4 w - - 0 1")

position.load(fen)

print(position)

#print(position.legal_moves)
print(position.legal_moves_dict.keys())