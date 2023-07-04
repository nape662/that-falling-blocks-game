from tetromino import *
from constants import *
import pygame as pg


# imports are already in constants.py


def cell_coordinates(x, y):
    return CELL_WIDTH * x, CELL_HEIGHT * y


def cell_rect(x, y):
    return CELL_WIDTH * x, CELL_HEIGHT * y, CELL_WIDTH, CELL_HEIGHT


class App:
    def __init__(self):
        self.running = False
        pg.init()
        pg.display.set_caption("Tetris")
        self.screen = pg.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.grid = self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.score = 0
        self.moving_piece = Tetromino(self)

    def max_drop_height(self):
        max_drop_height = 0
        while self.move_is_possible(0, max_drop_height + 1, 0):
            max_drop_height += 1
        return max_drop_height

    def move_is_possible(self, delta_x, delta_y, delta_rotation):
        for i, row in enumerate(self.moving_piece.rotated_shape(delta_rotation)):
            for j, cell in enumerate(row):
                try:
                    if cell == "O":
                        cell_y = self.moving_piece.y + delta_y + i
                        cell_x = self.moving_piece.x + delta_x + j
                        if self.grid[cell_y][cell_x] != 0 or \
                                cell_y >= HEIGHT or cell_x < 0:
                            return False  # doesn't even check for grid pos if "." and doesn't give Error
                except IndexError:
                    return False
        return True

    def move_piece(self, delta_x, delta_y, delta_rotation, hard_drop=False):
        rotated = 0
        if self.move_is_possible(delta_x, delta_y, delta_rotation):
            self.moving_piece.x += delta_x
            self.moving_piece.y += delta_y
            self.moving_piece.rotation += delta_rotation
            rotated = delta_rotation
        elif delta_rotation != 0:
            for i in (1, -1, 2, -2):
                if self.move_is_possible(i, 0, delta_rotation):
                    self.moving_piece.x += i
                    self.moving_piece.rotation += delta_rotation
                    rotated = delta_rotation
                    break
        self.draw_piece()
        if (rotated == 0 and not (self.move_is_possible(0, 1, 0)
                                  or self.move_is_possible(1, 0, 0)
                                  or self.move_is_possible(-1, 0, 0))) or hard_drop:
            self.fix_piece()

    def hard_drop(self):
        self.move_piece(0, self.max_drop_height(), 0, True)

    def fix_piece(self):
        for i, row in enumerate(self.moving_piece.rotated_shape()):
            for j, cell in enumerate(row):
                if cell == "O":
                    self.grid[self.moving_piece.y + i][self.moving_piece.x + j] = self.moving_piece.colour
        self.clear_lines()
        self.moving_piece = Tetromino(self)

    def clear_lines(self):
        for i, row in enumerate(self.grid):
            if 0 not in row:
                self.score += 100  # TODO better scoring system
                for k in range(i, 0, -1):
                    self.grid[k] = self.grid[k - 1]
                    for num, cell in enumerate(self.grid[k]):
                        if cell != 0:
                            self.screen.fill(cell, cell_rect(k, num))
                        else:
                            self.screen.fill(BLACK, cell_rect(k, num))

    def draw_piece(self):
        for i, row in enumerate(self.grid):  # here a little ineffective may be
            for j, cell in enumerate(row):
                if cell == 0:
                    self.screen.fill(BLACK, cell_rect(j, i))
        for i, row in enumerate(self.moving_piece.rotated_shape()):
            for j, cell in enumerate(row):
                try:
                    cell_x = self.moving_piece.x + j
                    cell_y = self.moving_piece.y + i
                    ghost_y = self.moving_piece.y + i + self.max_drop_height()
                    if cell == "O":
                        pg.draw.rect(self.screen, self.moving_piece.colour, cell_rect(cell_x, ghost_y), width=1)
                        self.screen.fill(self.moving_piece.colour, cell_rect(cell_x, cell_y))
                except IndexError:
                    pass


    def draw_game(self):
        self.draw_piece()
        pg.display.flip()

    def handle_inputs(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    if self.move_is_possible(1, 0, 0):
                        self.move_piece(1, 0, 0)
                elif event.key == pg.K_LEFT:
                    self.move_piece(-1, 0, 0)
                elif event.key == pg.K_UP:
                    self.move_piece(0, 0, 1)
                elif event.key == pg.K_DOWN:
                    self.move_piece(0, 1, 0)
                elif event.key == pg.K_SPACE:
                    self.hard_drop()
                self.draw_game()

    def run(self):
        self.running = True
        self.draw_game()
        while self.running:
            pg.time.Clock().tick_busy_loop(FPS)
            self.handle_inputs()
        return 0


Tetris = App()
Tetris.run()
