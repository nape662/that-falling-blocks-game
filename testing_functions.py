from constants import *

grid = [[0 for _ in range(3)] for _ in range(7)]

for i in range(7):
    grid[i] = [i for _ in range(3)]

grid[5] = [3, 3, 3]
print(grid)

def shit():
    for i, row in enumerate(grid):
        if all(cell != 0 for cell in row):
            del (grid[i])
            grid.insert(0, [0 for _ in range(3)])

def shittt():
    for i, row in enumerate(grid):
        if all(cell == 3 for cell in row):
            del(grid[i])
            grid.insert(0, [0 for _ in range(3)])

shittt()
print(grid)






