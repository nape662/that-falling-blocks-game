import pygame as pg
from random import randint, choice

FPS = 60
QUICK_DROP_EVENT = pg.event.custom_type()
REGULAR_DROP_EVENT = pg.event.custom_type()
FIX_PIECE_EVENT = pg.event.custom_type()
SPEEDY_DROP_RATE = 100
REGULAR_DROP_RATES = [999, 793, 618, 472, 355, 262, 189, 134, 94, 64, 42, 28, 18, 11, 7]
FIX_PIECE_DELAY = 500
FIX_PIECE_DELAY_STEP = 30
LINES_FOR_LEVELUP = 1


WIDTH = 10
HEIGHT = 20
GRID_PIXEL_WIDTH = 400
GRID_PIXEL_HEIGHT = 800
CELL_WIDTH = 40
CELL_HEIGHT = 40
WINDOW_WIDTH = GRID_PIXEL_WIDTH + CELL_WIDTH * 12
WINDOW_HEIGHT = 800
GRID_TOP_LEFT_X = CELL_WIDTH * 6
RIGHT_SIDE_X = GRID_PIXEL_WIDTH + CELL_WIDTH + GRID_TOP_LEFT_X
RIGHT_SIDE_WIDTH = CELL_WIDTH * 5
NEXT_PIECES_HEIGHT = CELL_HEIGHT * 10

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
        ['....',
         'OOOO',
         '....',
         '....'],
        ['..O.',
         '..O.',
         '..O.',
         '..O.'],
        ['....',
         '....',
         'OOOO',
         '....'],
        ['.O..',
         '.O..',
         '.O..',
         '.O..']
    ],
    [
        ['OO',
         'OO',
         ]
    ],
    [
        ['.O.', #0 up
         'OOO',
         '...'],
        ['.O.',
         '.OO',
         '.O.'],
        ['...',
         'OOO',
         '.O.'],
        ['.O.',
         'OO.',
         '.O.']
    ],
    [
        ['.OO',
         'OO.',
         '...'],
        ['.O.',
         '.OO',
         '..O'],
        ['...',
         '.OO',
         'OO.'],
        ['O..',
         'OO.',
         '.O.']
    ],
    [
        ['OO.',
         '.OO',
         '...'],
        ['..O',
         '.OO',
         '.O.'],
        ['...',
         'OO.',
         '.OO'],
        ['.O.',
         'OO.',
         'O..']
    ],
    [
        ['..O',
         'OOO',
         '...'],
        ['.O.',
         '.O.',
         '.OO'],
        ['...',
         'OOO',
         'O..'],
        ['OO.',
         '.O.',
         '.O.']
    ],
    [
        ['O..',
         'OOO',
         '...'],
        ['.OO',
         '.O.',
         '.O.'],
        ['...',
         'OOO',
         '..O'],
        ['.O.',
         '.O.',
         'OO.']
    ],
]


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

# Wall Kick Data
WALL_KICKS = {
    'OTHER': [
        [[(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)], [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]],
        [[(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)], [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]],
        [[(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)], [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]],
        [[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)], [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]]
    ],
    'I': [
        [[(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)], [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)]],
        [[(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)], [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)]],
        [[(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)], [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)]],
        [[(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)], [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)]]
          ]
}
