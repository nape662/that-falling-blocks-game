import pygame as pg
from random import randint, choice

FPS = 60
QUICK_DROP_EVENT = pg.event.custom_type()
REGULAR_DROP_EVENT = pg.event.custom_type()
FIX_PIECE_EVENT = pg.event.custom_type()
SPEEDY_DROP_RATE = 100
REGULAR_DROP_RATE = 500  # TODO: make this faster as the game progresses (shift this to App() class)
FIX_PIECE_DELAY = 300


WIDTH = 10
HEIGHT = 20
GRID_PIXEL_WIDTH = 400
GRID_PIXEL_HEIGHT = 800
CELL_WIDTH = GRID_PIXEL_WIDTH // WIDTH
CELL_HEIGHT = GRID_PIXEL_HEIGHT // HEIGHT
WINDOW_WIDTH = GRID_PIXEL_WIDTH + CELL_WIDTH * 6
WINDOW_HEIGHT = 800


GREEN = (125, 179, 73)
RED = (242, 26, 29)
BLUE = (0, 57, 255)
GHOST_BLUE = (3, 141, 252)
LIGHT_BLUE = (101, 197, 253)
YELLOW = (255, 227, 4)
PURPLE = (174, 56, 255)
GHOST_PURPLE = (255, 75, 255)
ORANGE = (255, 173, 0)
BLACK = (0, 0, 0)
PINK = (243, 114, 224)

COLOUR_LIST = [LIGHT_BLUE, YELLOW, PURPLE, GREEN, RED, ORANGE, BLUE]
GHOST_COLOUR_LIST = [LIGHT_BLUE, YELLOW, GHOST_PURPLE, GREEN, RED, ORANGE, GHOST_BLUE]  # ghost colours are lighter

# tetriminos
SHAPES = [
    [
        ['.....',
         '.....',
         'OOOO.',
         '.....',
         '.....'],
        ['.....',
         '.O...',
         '.O...',
         '.O...',
         '.O...'],
        ['.....',
         '.....'
         '.....',
         'OOOO.',
         '.....'],
        ['.....',
         '..O..',
         '..O..',
         '..O..',
         '..O..']
    ],
    [
        ['..',
         'OO',
         'OO',
         ]
    ],
    [
        ['.....',
         '.....',
         '..O..',
         '.OOO.'],
        ['.....',
         '..O..',
         '.OO..',
         '..O..'],
        ['.....',
         '.....',
         '.OOO.',
         '..O..'],
        ['.....',
         '..O..',
         '..OO.',
         '..O..']
    ],
    [
        [
         '.....',
         '.....',
         '..OO.',
         '.OO..'],
        ['.....',
         '.O...',
         '.OO..',
         '..O..']
    ],
    [
        ['.....',
         '.....',
         '.OO..',
         '..OO.',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '.O...',
         '.....']
    ],
    [
        ['.....',
         '...O.',
         '.OOO.',
         '.....',
         '.....'],
        ['.....',
         '.OO..',
         '..O..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '.O...',
         '.....'],
        ['.....',
         '..O..',
         '..O.',
         '..OO.',
         '.....']
    ],
    [
        ['.....',
         '.O...',
         '.OOO.',
         '.....',
         '.....'],
        ['.....',
         '..OO.',
         '..O..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '...O.',
         '.....'],
        ['.....',
         '..O..',
         '..O.',
         '.OO..',
         '.....']
    ],
]


# shapes for display on the right, only first rotation of each shape and with less padding

SHAPE_DISPLAYS = [
    ['OOOO'],
    ['.OO.',
     '.OO.'],
    ['..O..',
     '.OOO.'],
    ['..OO.',
     '.OO.'],
    ['.OO.',
     '..OO.'],
    ['...O.',
     '.OOO.'],
    ['.O...',
     '.OOO.']
]
