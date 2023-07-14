from tetromino import *
from constants import *
import pygame as pg

# imports are already in constants.py


def cell_rect(x, y):
    return CELL_WIDTH * x + GRID_TOP_LEFT_X, CELL_HEIGHT * y, CELL_WIDTH, CELL_HEIGHT


# TODO: learn logging module
# TODO: learn git add -i or -p

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
        # reset game
        self.level = 1
        self.score = 0
        self.combo = 0
        self.remaining_lines = LINES_FOR_LEVELUP
        self.t_spin = False
        self.mini_t_spin = False
        self.difficult_move = 1
        self.fall_rate = REGULAR_DROP_RATES[0]
        self.saved_piece = None
        self.already_switched = False
        self.moving_piece = Tetromino(self)
        self.next_pieces = [Tetromino(self, self.moving_piece.shape_number)]
        self.next_pieces += [Tetromino(self, self.next_pieces[i - 1].shape_number) for i in range(2)]
        self.draw_next_pieces()
        pg.time.set_timer(REGULAR_DROP_EVENT, self.fall_rate)
        pg.mixer.init(channels=1)
        pg.mixer.music.load("tetris_loop.mp3")
        pg.mixer.music.play(loops=-1)

    def reset_game(self):
        self.paused = False
        self.score = 0
        self.level = 1
        self.screen.fill((255, 255, 255), (GRID_PIXEL_WIDTH, 0, CELL_WIDTH, WINDOW_HEIGHT))
        self.screen.fill((255, 255, 255), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        self.draw_score()
        self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.moving_piece = Tetromino(self)
        self.next_pieces = [Tetromino(self, self.moving_piece.shape_number)]
        self.next_pieces += [Tetromino(self, self.next_pieces[i - 1].shape_number) for i in range(2)]
        pg.time.set_timer(REGULAR_DROP_EVENT, REGULAR_DROP_RATES[self.level] - 1)
        self.draw_game()
        # start music anew
        pg.mixer.music.play(loops=-1)

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
        # reset music
        pg.mixer.music.stop()

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
        if delta_rotation != 0:
            attempted_wall_kicks = WALL_KICKS["I" if self.moving_piece.shape_number == 0 else "OTHER"]
            for dx, dy in attempted_wall_kicks[self.moving_piece.rotation][0 if delta_rotation == -1 else 1]:  # we're not expecting 0 or 2 anyway
                if self.move_is_possible(dx, dy, delta_rotation):
                    self.moving_piece.x += dx
                    self.moving_piece.y += dy
                    self.moving_piece.rotation = (self.moving_piece.rotation + delta_rotation) % 4
                    moved = True
                    break
        else:
            if self.move_is_possible(delta_x, delta_y, 0):
                self.moving_piece.x += delta_x
                self.moving_piece.y += delta_y
                moved = True
        if moved:
            self.detect_t_spin(delta_rotation)
            self.draw_game()
            pg.time.set_timer(FIX_PIECE_EVENT, 0)
            if hard_drop:
                self.fix_piece()
        if not self.move_is_possible(0, 1, 0) and not self.paused:
            pg.time.set_timer(FIX_PIECE_EVENT, FIX_PIECE_DELAY-self.level*FIX_PIECE_DELAY_STEP)
        else:
            pg.time.set_timer(FIX_PIECE_EVENT, 0)

    def detect_t_spin(self, delta_rotation):
        if self.moving_piece.shape_number == 3 and delta_rotation != 0:
            filled_corners = 0
            corners = [(0, 0), (2, 0), (2, 2), (0, 2)]
            facing_corners = [corners[self.moving_piece.rotation], corners[(self.moving_piece.rotation + 1) % 4]]
            other_corners = [corners[(self.moving_piece.rotation + 2) % 4],
                             corners[(self.moving_piece.rotation + 3) % 4]]
            for i in facing_corners:
                if self.grid[self.moving_piece.y + i[1]][self.moving_piece.x + i[0]] != 0:
                    filled_corners += 1
            if filled_corners >= 3:
                if all((self.grid[self.moving_piece.y + i[1]][self.moving_piece.x + i[0]] != 0) \
                       for i in facing_corners):
                    self.score += 400 * self.level
                    self.t_spin = True
                else:
                    self.score += 100 * self.level
                    self.mini_t_spin = True

    def hard_drop(self):
        self.move_piece(0, self.max_drop_height(), 0, True)

    def fix_piece(self):
        self.t_spin = False
        self.mini_t_spin = False
        self.already_switched = False
        pg.time.set_timer(FIX_PIECE_EVENT, 0)
        for i, row in enumerate(self.moving_piece.rotated_shape()):
            for j, cell in enumerate(row):
                if cell == "O":
                    self.grid[self.moving_piece.y + i][self.moving_piece.x + j] = self.moving_piece.colour
        self.clear_lines()
        self.moving_piece = self.next_pieces.pop(0)
        self.next_pieces.append(Tetromino(self, self.next_pieces[-1].shape_number))
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
        cleared_lines = 0
        clear_line_scores = [0, 1, 3, 5, 8]
        for i, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                cleared_lines += 1
                del(self.grid[i])
                self.grid.insert(0, [0 for _ in range(WIDTH)])
        if cleared_lines > 0:
            if self.t_spin:
                if cleared_lines == 1:
                    self.score += 400 * self.level * self.difficult_move
                    lines_cleared_score = 3
                elif cleared_lines == 2:
                    self.score += 800 * self.level * self.difficult_move
                    lines_cleared_score = 5
                elif cleared_lines == 3:
                    self.score += 1200 * self.level * self.difficult_move
                    lines_cleared_score = 7
                self.difficult_move = 1.5
            elif self.mini_t_spin:
                self.score += 100 * clear_line_scores[cleared_lines] * self.level * self.difficult_move
                self.difficult_move = 1.5
            else:
                lines_cleared_score = clear_line_scores[cleared_lines]
                self.score += 100 * clear_line_scores[cleared_lines] * self.level * self.difficult_move
                if cleared_lines == 4:
                    self.difficult_move = 1.5
                else:
                    self.difficult_move = 1
            self.combo += 1
            self.score += 50 * self.combo * self.level
            lines_cleared_score = clear_line_scores[cleared_lines]
            while lines_cleared_score > 0:
                lines_cleared_score -= 1
                self.remaining_lines -= 1
                if self.remaining_lines == 0:
                    self.level += 1
                    self.remaining_lines = LINES_FOR_LEVELUP * self.level
                    pg.time.set_timer(REGULAR_DROP_EVENT, REGULAR_DROP_RATES[self.level]-1)
        elif not self.t_spin or not self.mini_t_spin:
            self.combo = -1

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

    def draw_level(self):
        level_font = pg.font.SysFont("Arial", 30)
        level_text = level_font.render("Level: " + str(self.level), True, BLACK)
        self.screen.blit(level_text, (RIGHT_SIDE_X, NEXT_PIECES_HEIGHT + 50))

    def draw_game(self):
        self.draw_grid()
        self.draw_moving_piece()
        self.draw_score()
        self.draw_next_pieces()
        self.draw_saved_piece()
        self.draw_level()
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
