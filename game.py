from position import Position
from fen import FenFile
import os

class Game:
    def __init__(self, str_fen):
        fen = FenFile()
        fen.from_string(str_fen)
        self.position = Position()
        self.position.load(fen)

    def print(self):
        os.system("cls")
        print(self.position)
        print(f"To move: {self.position.to_move.name}")

    def get_move(self):
        print(self.position.legal_moves_dict.keys())
        #print(self.position.legal_moves)
        while True:
            move = input("Input move: ")
            if move in self.position.legal_moves_dict.keys():
                return self.position.legal_moves_dict[move]
            print("Invalid move!")

    def run(self):
        while True:
            self.print()
            #print(self.position)
            self.position.move(self.get_move())