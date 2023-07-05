from constants import *


class Tetromino:
    def __init__(self, app, existing_shape_number=None):
        self.shape_number = choice([i for i in range(len(SHAPES)) if i != existing_shape_number])
        self.app = app
        self.rotation = 0
        self.shape = SHAPES[self.shape_number]
        self.colour = COLOUR_LIST[self.shape_number]
        self.x = WIDTH // 2 - 2
        self.y = -1

    def rotated_shape(self, delta_rotation=0):
        return self.shape[(self.rotation + delta_rotation) % len(self.shape)]



