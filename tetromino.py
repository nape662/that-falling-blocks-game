from constants import *


class Tetromino:
    def __init__(self, app):
        shape_number = 0  # randint(0, 5)
        self.app = app
        self.rotation = 0
        self.shape = SHAPES[shape_number][0]  # TODO: turn this into function from rotation
        self.colour = COLOUR_LIST[shape_number]
        self.x = WIDTH // 2 - 2
        self.y = 0




