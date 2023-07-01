from constants import *


class Tetromino:
    def __init__(self, app):
        shape_number = randint(1, 6)
        self.app = app
        self.shape = SHAPES[shape_number]
        self.colour = COLOUR_LIST[shape_number]
        self.x = WIDTH // 2
        self.y = 0
        self.rotation = 0




