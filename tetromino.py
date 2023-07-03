from constants import *


class Tetromino:
    def __init__(self, app):
        shape_number = randint(0, len(SHAPES) - 1)
        self.app = app
        self.rotation = 0
        self.shape = SHAPES[shape_number]
        self.colour = COLOUR_LIST[shape_number]
        self.x = WIDTH // 2 - 2
        self.y = -1

    def rotated_shape(self, delta_rotation=0):
        return self.shape[(self.rotation + delta_rotation) % len(self.shape)]



