import random

width = 10
height = 10
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


def display_maze(grid):
    print(" " + "_" * (len(grid[0]) * 2 - 1))
    for y, row in enumerate(grid):
        print("|", end="")
        for x, cell in enumerate(row):
            if x == 0 and y == 0:
                print('A', end='')
            elif x == len(row) - 1 and y == len(grid) - 1:
                print('B', end='')
            else:
                print(" " if cell & S else "_", end="")

            if cell & E:
                if x == len(row) - 1 and y == len(grid) - 1:
                    pass
                else:
                    print(" " if (cell | row[x + 1]) & S else "_", end="")
            else:
                print("|", end="")
        print()


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

display_maze(grid)

print(f"Maze generated with width={width}, height={height}, seed={seed}")
