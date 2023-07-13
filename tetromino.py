from constants import *


class Tetromino:
    def __init__(self, app, existing_shape_number=None, needed_shape_number=None):
        if needed_shape_number is not None:
            self.shape_number = needed_shape_number
        else:
            self.shape_number = choice([i for i in range(len(SHAPES)) if i != existing_shape_number])
        self.app = app
        self.rotation = 0
        self.shape = SHAPES[self.shape_number]
        self.colour = COLOUR_LIST[self.shape_number]
        # so if width is 3 then x should be 3
        # and if width is 4 then x should also be 3
        # but if width is 2 then x should be 4
        self.x = WIDTH // 2 - (len(self.shape[self.rotation][0]) + 1) // 2
        if self.shape_number == 0:
            print(self.x)
        self.y = 0

    def rotated_shape(self, delta_rotation=0):
        return self.shape[(self.rotation + delta_rotation) % len(self.shape)]





