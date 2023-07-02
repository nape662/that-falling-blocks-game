from tetromino import *
from constants import *
import pygame as pg
# imports are already in constants.py


def cell_coordinates(x, y):
    return CELL_WIDTH*x, CELL_HEIGHT*y


class App:
    def __init__(self):
        self.running = False
        pg.init()
        pg.display.set_caption("Tetris")
        self.screen = pg.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.surfaces = [[pg.Surface((CELL_WIDTH, CELL_HEIGHT)) for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.grid = self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        # TODO: improve surfaces / grid interaction, may be in a single class/structure
        self.score = 0
        self.moving_piece = Tetromino(self)

    def move_is_possible(self, delta_x, delta_y, delta_rotation):
        # no filled cells where "O"'s will be after setting to x, y
        for i, row in enumerate(self.moving_piece.shape[
                                    (self.moving_piece.rotation + delta_rotation) % len(self.moving_piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == "O" and self.grid[self.moving_piece.y+delta_y+i][self.moving_piece.x+delta_x+j] != 0:
                        return False  # doesn't even check for grid pos if "." and doesn't give Error
                except IndexError:
                    return False
        return True

    def move_piece(self, delta_x, delta_y, delta_rotation):
        self.moving_piece.x += delta_x
        self.moving_piece.y += delta_y
        self.moving_piece.rotation += delta_rotation
        self.draw_piece()

    def fix_piece(self):
        self.draw_piece()
        for i, row in enumerate(self.moving_piece.shape):
            for j, cell in enumerate(row):
                if cell == "O":
                    self.grid[self.moving_piece.y+i][self.moving_piece.x+j] = self.moving_piece.colour
        self.moving_piece = Tetromino(self)
        # check if we lost game

    def clear_lines(self):
        for i, row in enumerate(self.grid):
            if 0 not in row:
                self.score += 100  # TODO better scoring system
                row = self.grid[i-1]

    def draw_piece(self):
        # optimisation: only OOOO tetrimino fucks "only redraw shape" system up in exactly one cell
        try:
            if self.grid[self.moving_piece.y + 3][self.moving_piece.x - 1] == 0:
                self.surfaces[self.moving_piece.y + 3][self.moving_piece.x - 1].fill(BLACK)
                self.screen.blit(self.surfaces[self.moving_piece.y + 3][self.moving_piece.x - 1],
                                 dest=cell_coordinates((self.moving_piece.x - 1),
                                      (self.moving_piece.y + 3)))
        except IndexError:
            pass
        # here actual shape blit
        for i, row in enumerate(self.moving_piece.shape):
            for j, cell in enumerate(row):
                try:
                    if cell == "O":
                        self.surfaces[self.moving_piece.y+i][self.moving_piece.x+j].fill(self.moving_piece.colour)
                    elif self.grid[self.moving_piece.y+i][self.moving_piece.x+j] == 0:
                        self.surfaces[self.moving_piece.y + i][self.moving_piece.x + j].fill(BLACK)
                    self.screen.blit(self.surfaces[self.moving_piece.y + i][self.moving_piece.x + j],
                                     dest=cell_coordinates((self.moving_piece.x + j),
                                                           (self.moving_piece.y + i)))
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
                elif event.key == pg.K_LEFT and self.move_is_possible(-1, 0, 0):
                    self.move_piece(-1, 0, 0)
                elif event.key == pg.K_UP and self.move_is_possible(0, 0, 1):
                    self.move_piece(0, 0, 1)
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

