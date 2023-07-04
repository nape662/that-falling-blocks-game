import pygame as pg
from random import randint

FPS = 60

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800
WIDTH = 10
HEIGHT = 20
CELL_WIDTH = WINDOW_WIDTH // WIDTH
CELL_HEIGHT = WINDOW_HEIGHT // HEIGHT

GREEN = (125, 179, 73)
RED = (242, 26, 29)
BLUE = (69, 42, 233)
LIGHT_BLUE = (101, 197, 253)
YELLOW = (255, 227, 4)
PURPLE = (174, 56, 255)
ORANGE = (255, 173, 0)
BLACK = (0, 0, 0)

COLOUR_LIST = [LIGHT_BLUE, YELLOW, PURPLE, GREEN, RED, ORANGE, BLUE]

# tetriminos
SHAPES = [
    [
        ['.....',
         '.....'
         '.....',
         'OOOO.',
         '.....'],
        ['.....',
         '..O..',
         '..O..',
         '..O..',
         '..O..'],
        ['.....',
         '.....',
         'OOOO.',
         '.....',
         '.....'],
        ['.....',
         '.O...',
         '.O...',
         '.O...',
         '.O...']

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
         '.OOO.',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '..OO.',
         '..O..',
         '.....']
    ],
    [
        [
         '.....',
         '.....',
         '..OO.',
         '.OO..',
         '.....'],
        ['.....',
         '.O...',
         '.OO..',
         '..O..',
         '.....']
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
         '..O..',
         '..O.',
         '..OO.',
         '.....'],
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
         '.....']
    ],
    [
        ['.....',
         '..O..',
         '..O.',
         '.OO..',
         '.....'],
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
         '.....']
    ],
]

