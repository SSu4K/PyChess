import pygame
import json
from position import Position
from move import Flag, Type, Move
from piece import Color

file = open("assets/asset_config.json")
CONFIG = json.load(file)
file.close()
BLACK = CONFIG["colors"]["black_tile_color"]
WHITE = CONFIG["colors"]["white_tile_color"]
PIECE_SCALE = 0.9
textures = {}
for type in Type:
    if type == Type.EMPTY:
        continue
    textures[(type, Color.WHITE)] = pygame.image.load("assets/"+CONFIG["white_texture_paths"][type.value])
    textures[(type, Color.BLACK)] = pygame.image.load("assets/"+CONFIG["black_texture_paths"][type.value])

class DisplayBoard:
    def __init__(self):
        self.is_flipped = False
        self.pieces = []
        pass
    def load_position(self, position: Position):
        self.pieces = position.pieces
    def blit(self, surface: pygame.Surface):
        color_1 = BLACK
        color_2 = WHITE
        board_width = min(surface.get_size())
        tile_width = board_width/8
        pygame.draw.rect(surface, color_1, (0, 0, board_width, board_width))
        for i in range(0, 64, 2):
            y = (i//8)
            x = (i%8) + y%2
            pygame.draw.rect(surface, color_2, (x*tile_width, y*tile_width, tile_width, tile_width))

        for piece in self.pieces:
            x = piece.pos[0] * tile_width + (1-PIECE_SCALE)*tile_width/2
            y = piece.pos[1] * tile_width + (1-PIECE_SCALE)*tile_width/2
            scale = (PIECE_SCALE*tile_width, PIECE_SCALE*tile_width)
            surface.blit(pygame.transform.scale(textures[(piece.type, piece.color)], scale), (x, y))