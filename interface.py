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
HIGHLIGHT = CONFIG["colors"]["highlight_color"]
RECTANGLE_WIDTH = CONFIG["highlight_parameters"]["rectangle_width"]
CIRCLE_RADIUS = CONFIG["highlight_parameters"]["circle_radius"]

PIECE_SCALE = 0.8
SURFACE_RESOLUTION = 4096
TILE_RESOLUTION = SURFACE_RESOLUTION / 8
textures = {}
for type in Type:
    if type == Type.EMPTY:
        continue
    textures[(type, Color.WHITE)] = pygame.image.load(
        "assets/"+CONFIG["white_texture_paths"][type.value])
    textures[(type, Color.BLACK)] = pygame.image.load(
        "assets/"+CONFIG["black_texture_paths"][type.value])


class DisplayBoard:
    def __init__(self):
        self.is_flipped = False
        self.pieces = []
        self.position = None
        self.base_surface = pygame.Surface(
            (SURFACE_RESOLUTION, SURFACE_RESOLUTION))
        self.surface = pygame.Surface((SURFACE_RESOLUTION, SURFACE_RESOLUTION))

    def load_position(self, position: Position):
        self.position = position
        self.is_flipped = False
        if position.to_move == Color.BLACK:
            self.is_flipped = True
        self.pieces = position.pieces
        self.legal_moves = position.legal_moves
        self.generate_base_surface()

    def get_tile_pos(self, x, y):
        tile_width = SURFACE_RESOLUTION / 8
        if self.is_flipped:
            return [(7-x) * tile_width, y * tile_width]
        else:
            return [x * tile_width, (7-y) * tile_width]

    def generate_base_surface(self):
        color_1 = BLACK
        color_2 = WHITE
        board_width = SURFACE_RESOLUTION
        tile_width = board_width/8
        self.base_surface.fill(color_1)
        for i in range(0, 64, 2):
            y = (i//8)
            x = (i % 8) + y % 2
            pygame.draw.rect(self.base_surface, color_2,
                             (x*tile_width, y*tile_width, tile_width, tile_width))

        for piece in self.pieces:
            pos = self.get_tile_pos(piece.pos[0], piece.pos[1])
            pos[0] += (1-PIECE_SCALE)*tile_width/2
            pos[1] += (1-PIECE_SCALE)*tile_width/2
            scale = (PIECE_SCALE*tile_width, PIECE_SCALE*tile_width)
            self.base_surface.blit(pygame.transform.scale(
                textures[(piece.type, piece.color)], scale), pos)
        self.surface.blit(self.base_surface, (0, 0))

    def blit(self, surface: pygame.Surface):
        board_width = min(surface.get_size())
        surface.blit(pygame.transform.scale(
            self.surface, (board_width, board_width)), (0, 0))


class InteractiveBoard(DisplayBoard):
    def __init__(self):
        self.is_flipped = False
        self.pieces = []
        self.selected_moves = []
        self.base_surface = pygame.Surface(
            (SURFACE_RESOLUTION, SURFACE_RESOLUTION))
        self.surface = pygame.Surface((SURFACE_RESOLUTION, SURFACE_RESOLUTION))
        self.prev_mouse_pressed = False
        self.selected_piece = None

    def get_mouse_tile(self, mouse_pos, tile_width):
        x = int(mouse_pos[0]//(tile_width))
        y = int(mouse_pos[1]//(tile_width))
        if self.is_flipped:
            return [7-x, y]
        else:
            return [x, 7-y]

    def select_piece(self, mouse_tile):
        self.selected_moves = []
        self.selected_piece = None
        self.surface.blit(self.base_surface, (0, 0))
        for piece in self.pieces:
            if piece.pos[0] == mouse_tile[0] and piece.pos[1] == mouse_tile[1] and piece.color == self.position.to_move:
                self.selected_piece = piece
                tile_pos = self.get_tile_pos(mouse_tile[0], mouse_tile[1])
                pygame.draw.rect(self.surface, HIGHLIGHT,
                                 (tile_pos, (TILE_RESOLUTION, TILE_RESOLUTION)), RECTANGLE_WIDTH)

        if self.selected_piece != None:
            for move in self.legal_moves:
                if move.pos1 == self.selected_piece.pos:
                    self.selected_moves.append(move)
                    tile_pos = self.get_tile_pos(move.pos2[0], move.pos2[1])
                    if Flag.CAPTURE in move.flags:
                        pygame.draw.rect(
                            self.surface, HIGHLIGHT, (tile_pos, (TILE_RESOLUTION, TILE_RESOLUTION)), RECTANGLE_WIDTH)
                    else:
                        pygame.draw.circle(
                            self.surface, HIGHLIGHT, (tile_pos[0] + TILE_RESOLUTION/2, tile_pos[1] + TILE_RESOLUTION/2), CIRCLE_RADIUS)

    def get_move(self, surface: pygame.Surface) -> Move:
        surface_width = min(surface.get_size())
        x, y = pygame.mouse.get_pos()
        mouse_pos = (x-surface.get_rect().left, y-surface.get_rect().top)
        mouse_tile = self.get_mouse_tile(mouse_pos, surface_width/8)
        mouse_pressed = pygame.mouse.get_pressed(
        )[0] and not self.prev_mouse_pressed
        self.prev_mouse_pressed = pygame.mouse.get_pressed()[0]
        
        if mouse_pressed:
            if self.selected_piece == None:
                self.select_piece(mouse_tile)
            else:
                for move in self.selected_moves:
                    if move.pos2[0] == mouse_tile[0] and move.pos2[1] == mouse_tile[1]:
                        self.selected_piece = None
                        return move
                self.select_piece(mouse_tile)

        return None
