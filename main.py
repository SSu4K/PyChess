from game import Game
from interface import DisplayBoard
from fen import FenFile
from position import Position
import pygame
game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
#game = Game("r2qkbnr/ppp2ppp/2npb3/4p3/2B1P3/2N5/PPPP1NPP/R1BQK2R w KQkq - 0 1")
#game.run()

BACKGROUND_COLOR = (25, 25, 25)
WHITE = (255, 255, 255)
RED = (200, 50, 100)
GREEN = (50, 200, 100)

WINDOW_SIZE = (800, 500)

pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
surface = pygame.display.get_surface()

board = DisplayBoard()
board.load_position(game.position)
run = True
while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    surface.fill(GREEN)
    board.blit(surface)
    pygame.display.flip()