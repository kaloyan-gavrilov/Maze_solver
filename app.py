import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from generator import create_maze, convert_to_wall_grid, write_maze_file
from solver import Maze

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Generator and Solver")

        self.left_frame = ttk.Frame(root, padding="10")
        self.left_frame.grid(row=0, column=0, sticky="ns")

        self.label_width = ttk.Label(self.left_frame, text="Width:")
        self.label_width.grid(row=0, column=0, padx=5, pady=5)
        self.entry_width = ttk.Entry(self.left_frame)
        self.entry_width.grid(row=0, column=1, padx=5, pady=5)

        self.label_height = ttk.Label(self.left_frame, text="Height:")
        self.label_height.grid(row=1, column=0, padx=5, pady=5)
        self.entry_height = ttk.Entry(self.left_frame)
        self.entry_height.grid(row=1, column=1, padx=5, pady=5)

        self.generate_button = ttk.Button(self.left_frame, text="Generate Maze", command=self.generate_maze)
        self.generate_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.show_explored = tk.BooleanVar()
        self.show_explored_check = ttk.Checkbutton(self.left_frame, text="Show Explored", variable=self.show_explored)
        self.show_explored_check.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.solve_button = ttk.Button(self.left_frame, text="Solve Maze", command=self.solve_maze)
        self.solve_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.canvas = Canvas(root, width=600, height=600, bg="white")
        self.canvas.grid(row=0, column=1, padx=10, pady=10)

        self.maze = None

    def generate_maze(self):
        width = int(self.entry_width.get())
        height = int(self.entry_height.get())

        maze_grid = create_maze(width, height)
        wall_grid = convert_to_wall_grid(maze_grid, width, height)
        write_maze_file(wall_grid, "maze_used_for_main_app")
        self.maze = Maze("maze_used_for_main_app.txt")

        self.draw_maze()

    def solve_maze(self):
        if self.maze is None:
            return

        self.maze.solve()
        self.draw_maze(solved=True)

    def draw_maze(self, solved=False):
        self.canvas.delete("all")
        cell_size = min(600 // self.maze.width, 600 // self.maze.height)

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                color = "#ededfc"
                if self.maze.walls[y][x] == 1:
                    color = "#282828"
                elif (y, x) == self.maze.start:
                    color = "#00ab1c"
                elif (y, x) == self.maze.goal:
                    color = "#ff0000"
                elif solved and self.maze.solution and (y, x) in self.maze.solution[1]:
                    color = "#dceb71"
                elif solved and self.show_explored.get() and (y, x) in self.maze.explored:
                    color = "#d46155"

                x1, y1 = x * cell_size, y * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=1)


root = tk.Tk()
app = MazeApp(root)
root.mainloop()
