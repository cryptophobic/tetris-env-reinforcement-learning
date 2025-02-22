import numpy as np
import pygame

from application import config
from application.Piece import Piece
from application.renderer.Renderer import Renderer


class Graphics(Renderer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pygame.init()
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE, 0, 32)
        pygame.display.set_caption("Hello Tetris")
        self.screen.fill((0, 0, 0))

    def __del__(self):
        pygame.quit()

    def render(self, piece: Piece|None):
        self.screen.fill((0, 0, 0))

        shape = piece.shape

        for y, x in np.ndindex(shape.shape):
            if shape[y, x] == 0:
                continue
            rect = pygame.Rect(
                ((piece.x + x) * config.BLOCK_WIDTH) + config.BORDERS_WIDTH,
                ((piece.y + y) * config.BLOCK_HEIGHT) + config.BORDERS_HEIGHT,
                config.BLOCK_WIDTH - config.BORDERS_WIDTH  * 2,
                config.BLOCK_HEIGHT - config.BORDERS_HEIGHT * 2)

            pygame.draw.rect(self.screen, piece.color, rect)

        for y, x in np.ndindex(self.board.board.shape):
            if self.board.board[y, x] == 0:
                continue

            rect = pygame.Rect(
                (x * config.BLOCK_WIDTH) + config.BORDERS_WIDTH,
                (y * config.BLOCK_HEIGHT) + config.BORDERS_HEIGHT,
                config.BLOCK_WIDTH - config.BORDERS_WIDTH  * 2,
                config.BLOCK_HEIGHT - config.BORDERS_HEIGHT * 2)
            pygame.draw.rect(self.screen, (255, 255, 0), rect)

        pygame.display.update()
