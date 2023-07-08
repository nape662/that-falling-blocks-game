from tetromino import *
from constants import *
import pygame as pg

# imports are already in constants.py


def cell_rect(x, y):
    return CELL_WIDTH * x + GRID_TOP_LEFT_X, CELL_HEIGHT * y, CELL_WIDTH, CELL_HEIGHT


class App:
    def __init__(self):
        self.running = False
        self.paused = False
        pg.init()
        pg.display.set_caption("Tetris")
        self.clock = pg.time.Clock()
        # drawing stuff
        self.screen = pg.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        # next lines are self.reset_game()
        self.screen.fill((255, 255, 255), (GRID_TOP_LEFT_X - CELL_WIDTH, 0, CELL_WIDTH, WINDOW_HEIGHT))
        self.screen.fill((255, 255, 255), (0, CELL_WIDTH * 3,
                                           RIGHT_SIDE_WIDTH, WINDOW_HEIGHT - CELL_WIDTH * 3))
        self.screen.fill((255, 255, 255), (GRID_PIXEL_WIDTH+GRID_TOP_LEFT_X, 0, CELL_WIDTH, WINDOW_HEIGHT))
        self.screen.fill((255, 255, 255), (RIGHT_SIDE_X, NEXT_PIECES_HEIGHT,
                                           RIGHT_SIDE_WIDTH, WINDOW_HEIGHT-NEXT_PIECES_HEIGHT))
        self.grid_lines_surface = pg.Surface((GRID_PIXEL_WIDTH, GRID_PIXEL_HEIGHT))
        self.grid_lines_surface.set_alpha(50)
        self.paused = False
        self.score = 0
        self.saved_piece = None
        self.already_switched = False
        self.moving_piece = Tetromino(self)
        self.next_pieces = [Tetromino(self, self.moving_piece.shape_number)]
        self.next_pieces += [Tetromino(self, self.next_pieces[i - 1].shape_number) for i in range(2)]
        self.draw_next_pieces()
        pg.time.set_timer(REGULAR_DROP_EVENT, REGULAR_DROP_RATE)

    def reset_game(self):
        self.paused = False
        self.score = 0
        self.screen.fill((255, 255, 255), (GRID_PIXEL_WIDTH, 0, CELL_WIDTH, WINDOW_HEIGHT))
        self.draw_score()
        self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.moving_piece = Tetromino(self)
        self.next_pieces = [Tetromino(self, self.moving_piece.shape_number)]
        self.next_pieces += [Tetromino(self, self.next_pieces[i - 1].shape_number) for i in range(2)]
        self.draw_game()

    def game_over(self):
        self.paused = True
        self.already_switched = False
        self.draw_score()
        self.draw_game()
        bold_font = pg.font.SysFont("Arial", 100)
        small_font = pg.font.SysFont("Arial", 50)
        game_over_text = bold_font.render("GAME OVER", True, PINK)
        reset_text = small_font.render("Press SPACE to play again", True, GHOST_BLUE)
        a, b = (game_over_text.get_size())
        c, d = (reset_text.get_size())
        self.screen.blit(game_over_text, (WINDOW_WIDTH / 2 - a / 2, WINDOW_HEIGHT / 2 - b / 2))
        self.screen.blit(reset_text, (WINDOW_WIDTH / 2 - c / 2, WINDOW_HEIGHT / 2 - d / 2 + b))
        pg.display.flip()
        # reset timers
        pg.time.set_timer(QUICK_DROP_EVENT, 0)
        pg.time.set_timer(FIX_PIECE_EVENT, 0)

    def switch_piece(self):
        if not self.already_switched:
            if self.saved_piece is None:  # reset in case of game over
                self.saved_piece = Tetromino(self, needed_shape_number=self.moving_piece.shape_number)
                self.moving_piece = self.next_pieces.pop(0)
                self.next_pieces.append(Tetromino(self, self.next_pieces[-1].shape_number))
            else:
                self.moving_piece, self.saved_piece = self.saved_piece, self.moving_piece
                self.saved_piece = Tetromino(self, needed_shape_number=self.saved_piece.shape_number)  # to reset x and y
            self.already_switched = True
            self.draw_game()
        else:
            pass

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
        moved = False
        if self.move_is_possible(delta_x, delta_y, delta_rotation):
            self.moving_piece.x += delta_x
            self.moving_piece.y += delta_y
            self.moving_piece.rotation += delta_rotation
            moved = True
        elif delta_rotation != 0:
            for i in (1, -1, 2, -2):
                if self.move_is_possible(i, 0, delta_rotation):
                    self.moving_piece.x += i
                    self.moving_piece.rotation += delta_rotation
                    moved = True
                    break
        if moved:
            self.draw_game()
            if hard_drop:
                pg.time.set_timer(FIX_PIECE_EVENT, 0)
                self.fix_piece()
        if not self.move_is_possible(0, 1, 0) and not self.paused:
            pg.time.set_timer(FIX_PIECE_EVENT, FIX_PIECE_DELAY)
        else:
            pg.time.set_timer(FIX_PIECE_EVENT, 0)

    def hard_drop(self):
        self.move_piece(0, self.max_drop_height(), 0, True)

    def fix_piece(self):
        pg.time.set_timer(FIX_PIECE_EVENT, 0)
        for i, row in enumerate(self.moving_piece.rotated_shape()):
            for j, cell in enumerate(row):
                if cell == "O":
                    self.grid[self.moving_piece.y + i][self.moving_piece.x + j] = self.moving_piece.colour
        self.clear_lines()
        self.moving_piece = self.next_pieces.pop(0)
        self.next_pieces.append(Tetromino(self, self.next_pieces[-1].shape_number))
        self.already_switched = False
        self.draw_game()
        if not self.move_is_possible(0, 0, 0):
            self.game_over()

    def draw_grid_lines(self):
        for i in range(1, WIDTH+1):
            pg.draw.line(self.grid_lines_surface, (255, 255, 255),
                         (i * CELL_WIDTH, 0), (i * CELL_WIDTH, GRID_PIXEL_HEIGHT))
        for i in range(1, HEIGHT):
            pg.draw.line(self.grid_lines_surface, (255, 255, 255),
                         (0, i * CELL_HEIGHT), (GRID_PIXEL_WIDTH, i * CELL_HEIGHT))
        self.screen.blit(self.grid_lines_surface, (GRID_TOP_LEFT_X, 0))

    def draw_next_pieces(self):
        self.screen.fill(BLACK, (RIGHT_SIDE_X, 0, RIGHT_SIDE_WIDTH, NEXT_PIECES_HEIGHT))
        for i, piece in enumerate(self.next_pieces):
            little_x_shift = 0.5 if piece.shape_number == 0 or piece.shape_number == 1 else 0
            little_y_shift = 0.5 if piece.shape_number == 0 else 0
            for j, row in enumerate(SHAPE_DISPLAYS[piece.shape_number]):
                for k, cell in enumerate(row):
                    if cell == "O":
                        self.screen.fill(piece.colour, cell_rect(11 + k + little_x_shift, 1 + 3 * i + j + little_y_shift))

    def draw_saved_piece(self):
        self.screen.fill(BLACK, (0, 0, RIGHT_SIDE_WIDTH, CELL_HEIGHT * 6))
        if self.saved_piece is not None:
            little_shift = 0.5 if self.saved_piece.shape_number == 0 or self.saved_piece.shape_number == 1 else 0
            little_y_shift = 0.5 if self.saved_piece.shape_number == 0 else 0
            for i, row in enumerate(SHAPE_DISPLAYS[self.saved_piece.shape_number]):
                for j, cell in enumerate(row):
                    if cell == "O":
                        self.screen.fill(self.saved_piece.colour, cell_rect(j + little_shift - 6, 2 + i + little_y_shift))

    def clear_lines(self):
        for i, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                self.score += 100  # TODO look official Tetris scoring system
                del(self.grid[i])
                self.grid.insert(0, [0 for _ in range(WIDTH)])

    def draw_grid(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == 0:
                    self.screen.fill(BLACK, cell_rect(j, i))
        self.draw_grid_lines()
        for k, row in enumerate(self.grid):
            for num, cell in enumerate(row):
                if cell != 0:
                    self.screen.fill(cell, cell_rect(num, k))

    def draw_moving_piece(self):
        for i, row in enumerate(self.moving_piece.rotated_shape()):
            for j, cell in enumerate(row):
                try:
                    cell_x = self.moving_piece.x + j
                    cell_y = self.moving_piece.y + i
                    ghost_y = self.moving_piece.y + i + self.max_drop_height()
                    if cell == "O":
                        pg.draw.rect(self.screen, GHOST_COLOUR_LIST[self.moving_piece.shape_number], cell_rect(cell_x, ghost_y), width=1)
                        self.screen.fill(self.moving_piece.colour, cell_rect(cell_x, cell_y))
                except IndexError:
                    pass

    def draw_score(self):
        score_font = pg.font.SysFont("Arial", 30)
        score_text = score_font.render("Score: " + str(self.score), True, BLACK)
        self.screen.fill((255, 255, 255), (RIGHT_SIDE_X, NEXT_PIECES_HEIGHT + 10,
                                           RIGHT_SIDE_WIDTH, WINDOW_HEIGHT - NEXT_PIECES_HEIGHT))
        self.screen.blit(score_text, (RIGHT_SIDE_X, NEXT_PIECES_HEIGHT + 10))

    def draw_game(self):
        self.draw_grid()
        self.draw_moving_piece()
        self.draw_score()
        self.draw_next_pieces()
        self.draw_saved_piece()
        pg.display.flip()

    def handle_inputs(self):
        if not self.paused:
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
                        pg.time.set_timer(QUICK_DROP_EVENT, SPEEDY_DROP_RATE)
                    elif event.key == pg.K_SPACE:
                        self.hard_drop()
                    elif event.key == pg.K_z or event.key == pg.K_y:  # on behalf of deutsches Tastatur-Layout
                        self.move_piece(0, 0, -1)
                    elif event.key == pg.K_c:
                        self.switch_piece()
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_DOWN:
                        pg.time.set_timer(QUICK_DROP_EVENT, 0)
                elif event.type == QUICK_DROP_EVENT or event.type == REGULAR_DROP_EVENT:
                    self.move_piece(0, 1, 0)
                elif event.type == FIX_PIECE_EVENT:
                    self.fix_piece()
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    break
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.reset_game()
                        self.draw_game()

    def run(self):
        self.running = True
        self.draw_game()
        while self.running:
            self.clock.tick_busy_loop(FPS)
            self.handle_inputs()
        return 0


Tetris = App()
Tetris.run()
