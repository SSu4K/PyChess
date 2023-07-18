from game import Game
from interface import DisplayBoard, InteractiveBoard
from fen import FenFile
from position import Position
from bot import CaptureBot, RandomBot, ExchangeBot
import pygame
import random
game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
#game = Game("r2qkbnr/ppp2ppp/2npb3/4p3/2B1P3/2N5/PPPP1NPP/R1BQK2R w KQkq - 0 1")
#game.run()

BACKGROUND_COLOR = (25, 25, 25)
WHITE = (255, 255, 255)
RED = (200, 50, 100)
GREEN = (50, 200, 100)

WINDOW_SIZE = (600, 600)

pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
surface = pygame.display.get_surface()

bot = ExchangeBot()

board = InteractiveBoard()
board.load_position(game.position)
run = True
while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    surface.fill(GREEN)
    move = board.get_move(surface)
    
    if move != None:
        game.position.move(move)
        game.position.move(bot.get_move(game.position))
        board.load_position(game.position)

    board.blit(surface)
    pygame.display.flip()