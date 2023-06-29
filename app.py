
from constants import *
import pygame as pg


class App:
    def __init__(self, width, height):
        pg.init()
        pg.display.set_caption("Dots")
        self.screen = pg.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

        self.width = width
        self.height = height
        self.grid = self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.score = 0

