from position import Position
from fen import FenFile

fen = FenFile()
position = Position()

fen.from_string("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")

position.load(fen)

print(position)