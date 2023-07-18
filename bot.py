from position import Position, Flag, Type
from move import Move
from copy import deepcopy
import random

class Bot:
    def __init__(self):
        pass
    
    def move_heuristic(self, position: Position, move: Move) -> float:
        return 0

    def get_move(self, position: Position) -> Move:
        moves = deepcopy(position.legal_moves)
        random.shuffle(moves)
        return max(moves, key=lambda x: self.move_heuristic(position, x))

class RandomBot(Bot):
    pass

class CaptureBot(Bot):
    def move_heuristic(self, position: Position, move: Move) -> float:
        if Flag.CAPTURE in move.flags:
            return 1
        return 0    
    
class ExchangeBot(Bot):
    def move_heuristic(self, position: Position, move: Move) -> float:
        if Flag.CAPTURE in move.flags:
            value_1 = position.board[move.pos1[0]][move.pos1[1]].value
            value_2 = position.board[move.pos2[0]][move.pos2[1]].value
            if value_1 == value_2:
                return 1
        return 0 
