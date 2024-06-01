import random
from collections import deque

seed = random.randint(0, 0xFFFFFFFF)

random.seed(seed)

N, S, E, W = 1, 2, 4, 8
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {E: W, W: E, N: S, S: N}


class Tree:
    def __init__(self):
        self.parent = None

    def root(self):
        return self.parent.root() if self.parent else self

    def connected(self, tree):
        return self.root() == tree.root()

    def connect(self, tree):
        tree.root().parent = self


def create_maze(width, height):
    grid = [[0] * width for _ in range(height)]
    sets = [[Tree() for _ in range(width)] for _ in range(height)]

    edges = []
    for y in range(height):
        for x in range(width):
            if y > 0:
                edges.append((x, y, N))
            if x > 0:
                edges.append((x, y, W))
    random.shuffle(edges)

    while edges:
        x, y, direction = edges.pop()
        nx, ny = x + DX[direction], y + DY[direction]

        set1, set2 = sets[y][x], sets[ny][nx]

        if not set1.connected(set2):
            set1.connect(set2)
            grid[y][x] |= direction
            grid[ny][nx] |= OPPOSITE[direction]

    return grid


def convert_to_wall_grid(grid, width, height):
    wall_grid = [[1] * (width * 2 + 1) for _ in range(height * 2 + 1)]

    for y in range(height):
        for x in range(width):
            cy, cx = y * 2 + 1, x * 2 + 1
            wall_grid[cy][cx] = 0
            if grid[y][x] & S:
                wall_grid[cy + 1][cx] = 0
            if grid[y][x] & E:
                wall_grid[cy][cx + 1] = 0

    return wall_grid


def write_maze_file(wall_grid, file_name):
    with open(f"{file_name}.txt", "w") as writer:
        for y in range(len(wall_grid)):
            for x in range(len(wall_grid[y])):
                if (y, x) == (1, 1):
                    writer.write('A')
                elif (y, x) == (len(wall_grid) - 2, len(wall_grid[y]) - 2):
                    writer.write('B')
                else:
                    writer.write('1' if wall_grid[y][x] == 1 else ' ')
            writer.write('\n')

# width = int(input("Enter the width of the maze: "))
# height = int(input("Enter the height of the maze: "))
# name = input("Enter name of the file: ")
# maze_grid = create_maze(width, height)
# wall_grid = convert_to_wall_grid(maze_grid)
# write_maze_file(wall_grid, name)

# print(f"Maze generated with width={width}, height={height}, seed={seed}")
