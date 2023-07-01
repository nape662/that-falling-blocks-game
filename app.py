from tetromino import *
from constants import *
import pygame as pg
# imports are already in constants.py


class App:
    def __init__(self, width, height):
        pg.init()
        pg.display.set_caption("Dots")
        self.screen = pg.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

        self.width = width
        self.height = height
        self.grid = self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.score = 0

        self.moving_piece = Tetromino(self)

    def check_move(self, delta_x, delta_y, delta_rotation):
        # no filled cells where "O"'s will be after setting to x, y
        for i, row in enumerate(self.moving_piece.shape[(self.moving_piece.rotation + delta_rotation) % len(self.moving_piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == "O" and self.grid[self.moving_piece.y+delta_y+i][self.moving_piece.x+delta_x+j] != 0:
                        return False  # doesn't even check for grid pos if "." and doesn't give Error
                except IndexError:
                    return False
        return True

    def move_piece(self, delta_x, delta_y, delta_rotation):
        self.check_move(delta_x, delta_y, delta_rotation)
        self.moving_piece.x += delta_x
        self.moving_piece.y += delta_y
        self.moving_piece.rotation += delta_rotation
        self.draw_piece()

    def fix_piece(self):
        self.draw_piece()
        for i, row in enumerate(self.moving_piece.shape):
            for j, cell in enumerate(row):
                if cell == "O":
                    self.grid[self.moving_piece.y+i][self.moving_piece.x+j] += self.moving_piece.colour
        self.moving_piece = Tetromino(self)
        # check if we lost game

    def clear_lines(self):
        for i, row in enumerate(self.grid):
            if 0 not in row:
                self.score += 100  # TODO better scoring system
                row = self.grid[i-1]

    def draw_piece(self):
        pass

    def run(self):
        pass


Tetris = App(WIDTH, HEIGHT)
Tetris.run()

