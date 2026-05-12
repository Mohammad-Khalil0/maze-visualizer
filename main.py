import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import random
import time
from PIL import Image, ImageTk

# Maze Graph class
class MazeGraph:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [['open' for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.end = None
        self.graph = {}
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    def generate_maze(self, wall_percentage=0.3):
        """Randomly generate walls and open spaces for the maze."""
        for r in range(self.rows):
            for c in range(self.cols):
                if random.random() < wall_percentage:  # wall_percentage chance for a wall
                    self.grid[r][c] = 'wall'
                else:
                    self.grid[r][c] = 'open'

        # Set random start and end points
        self.start = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
        self.end = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
        self.grid[self.start[0]][self.start[1]] = 'start'
        self.grid[self.end[0]][self.end[1]] = 'end'

    def is_valid_move(self, r, c):
        """Check if a move is within the grid and not a wall."""
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != 'wall'

    def a_star(self):
        """A* pathfinding algorithm."""
        open_list = []
        heapq.heappush(open_list, (0 + self.heuristic(self.start), 0, self.start))  # f, g, position
        came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start)}

        while open_list:
            _, current_g, current_node = heapq.heappop(open_list)

            if current_node == self.end:
                return self.reconstruct_path(came_from)

            for dr, dc in self.directions:
                nr, nc = current_node[0] + dr, current_node[1] + dc
                if self.is_valid_move(nr, nc):
                    tentative_g_score = current_g + 1
                    if (nr, nc) not in g_score or tentative_g_score < g_score[(nr, nc)]:
                        came_from[(nr, nc)] = current_node
                        g_score[(nr, nc)] = tentative_g_score
                        f_score[(nr, nc)] = tentative_g_score + self.heuristic((nr, nc))
                        heapq.heappush(open_list, (f_score[(nr, nc)], tentative_g_score, (nr, nc)))

        return []

    def heuristic(self, node):
        """Heuristic for A* algorithm (Manhattan distance)."""
        return abs(node[0] - self.end[0]) + abs(node[1] - self.end[1])

    def reconstruct_path(self, came_from):
        """Reconstruct the path from the start to the end."""
        path = []
        current_node = self.end
        while current_node != self.start:
            path.append(current_node)
            current_node = came_from[current_node]
        path.append(self.start)
        path.reverse()
        return path

# Enhanced Maze Solver Game with added features for user interactivity and options
class MazeSolverApp:
    def __init__(self, root, maze):
        self.root = root
        self.maze = maze
        self.cell_size = 40
        self.drawing = False  # Track whether the user is in drawing mode
        self.canvas = tk.Canvas(self.root, width=self.maze.cols * self.cell_size,
                                height=self.maze.rows * self.cell_size, bg="white")
        self.canvas.pack(side='left')

        # Sidebar for user options
        self.sidebar = tk.Frame(self.root, width=200, bg='lightgray', height=self.maze.rows * self.cell_size)
        self.sidebar.pack(side='right', fill='y')

        # Add input fields for maze size (rows and columns)
        self.maze_size_label = tk.Label(self.sidebar, text="Maze Size (Rows x Columns)")
        self.maze_size_label.pack(pady=5)
        self.rows_entry = tk.Entry(self.sidebar)
        self.rows_entry.insert(0, str(self.maze.rows))
        self.rows_entry.pack(pady=5)
        self.cols_entry = tk.Entry(self.sidebar)
        self.cols_entry.insert(0, str(self.maze.cols))
        self.cols_entry.pack(pady=5)

        # Update maze size button
        self.update_size_button = ttk.Button(self.sidebar, text="Update Maze Size", command=self.update_maze_size)
        self.update_size_button.pack(pady=5)

        self.generate_maze_button = ttk.Button(self.sidebar, text="Generate Maze", command=self.generate_maze)
        self.generate_maze_button.pack(pady=5)

        self.solve_button = ttk.Button(self.sidebar, text="Solve Maze", command=self.solve_maze)
        self.solve_button.pack(pady=5)

        self.reset_button = ttk.Button(self.sidebar, text="Reset", command=self.reset_game)
        self.reset_button.pack(pady=5)

        self.randomize_button = ttk.Button(self.sidebar, text="Random Maze", command=self.randomize_maze)
        self.randomize_button.pack(pady=5)

        self.wall_percentage_label = tk.Label(self.sidebar, text="Wall Density")
        self.wall_percentage_label.pack(pady=5)
        self.wall_density = tk.Scale(self.sidebar, from_=10, to=90, orient="horizontal")
        self.wall_density.set(30)  # Default 30%
        self.wall_density.pack(pady=5)

        self.start_time = None

        # Load the walking image
        self.walking_image = Image.open("character.png")  # Replace with your image path
        self.walking_image = self.walking_image.resize((self.cell_size, self.cell_size))
        self.walking_photo = ImageTk.PhotoImage(self.walking_image)

        # Load the wall texture image
        self.wall_texture = Image.open("wall_texture.jpg")  # Replace with your image path
        self.wall_texture = self.wall_texture.resize((self.cell_size, self.cell_size))
        self.wall_texture_photo = ImageTk.PhotoImage(self.wall_texture)

        # Load the door image
        self.door_image = Image.open("door.png")  # Replace with your image path
        self.door_image = self.door_image.resize((self.cell_size, self.cell_size))
        self.door_photo = ImageTk.PhotoImage(self.door_image)

        # Create image item for the walking character
        self.character = None  # Initially set to None

        # Bind mouse click to canvas for maze drawing
        self.canvas.bind("<Button-1>", self.toggle_wall)

        # Start the maze generation process
        self.generate_maze()

    def toggle_wall(self, event):
        """Toggle wall at the clicked location."""
        row, col = self.get_cell_from_event(event)

        if self.maze.grid[row][col] == 'wall':
            self.maze.grid[row][col] = 'empty'
        else:
            self.maze.grid[row][col] = 'wall'

        # After toggling, redraw the maze and ensure the character is placed
        self.draw_maze()  # Redraw the entire maze
        self.ensure_character_position()  # Ensure the character is correctly placed
        self.character = self.canvas.create_image(self.maze.start[1] * self.cell_size + self.cell_size // 2,
                                                  self.maze.start[0] * self.cell_size + self.cell_size // 2,
                                                  image=self.walking_photo)

    def ensure_character_position(self):
        """Ensure the character stays at the start position after maze update."""
        # If the character is not already created, initialize it.
        if not self.character:
            self.character = self.canvas.create_image(self.maze.start[1] * self.cell_size + self.cell_size // 2,
                                                      self.maze.start[0] * self.cell_size + self.cell_size // 2,
                                                      image=self.walking_photo)
        # Update the character's position to the start position (in case it was moved or removed).
        self.canvas.coords(self.character, self.maze.start[1] * self.cell_size + self.cell_size // 2,
                           self.maze.start[0] * self.cell_size + self.cell_size // 2)

    def get_cell_from_event(self, event):
        """Get the row and column of the cell from a mouse click event."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        return row, col

    def generate_maze(self):
        """Generate the maze with random walls and a random start and end."""
        self.maze.generate_maze(wall_percentage=self.wall_density.get() / 100)
        self.draw_maze()

    def draw_maze(self):
        """Draw the maze with walls, start, and end points."""
        self.canvas.delete("all")
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                x = col * self.cell_size
                y = row * self.cell_size

                if self.maze.grid[row][col] == 'wall':
                    self.canvas.create_image(x, y, image=self.wall_texture_photo, anchor='nw')
                elif self.maze.grid[row][col] == 'start':
                    self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="green")
                elif self.maze.grid[row][col] == 'end':
                    self.canvas.create_image(x, y, image=self.door_photo, anchor='nw')

        # If the character is not initialized, create it.
        if not self.character:
            self.character = self.canvas.create_image(self.maze.start[1] * self.cell_size + self.cell_size // 2,
                                                      self.maze.start[0] * self.cell_size + self.cell_size // 2,
                                                      image=self.walking_photo)

        # Draw the character's starting position (this ensures the character is drawn).
        self.canvas.coords(self.character, self.maze.start[1] * self.cell_size + self.cell_size // 2,
                           self.maze.start[0] * self.cell_size + self.cell_size // 2)

    def update_maze_size(self):
        """Update the maze size based on user input."""
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            self.maze = MazeGraph(rows, cols)
            self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)
            self.generate_maze()  # Regenerate the maze
            # Recreate the character after resizing the maze
            self.character = self.canvas.create_image(self.maze.start[1] * self.cell_size + self.cell_size // 2,
                                                      self.maze.start[0] * self.cell_size + self.cell_size // 2,
                                                      image=self.walking_photo)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for rows and columns.")

    def solve_maze(self):
        """Solve the maze using A* algorithm and animate the path."""
        path = self.maze.a_star()
        if not path:
            messagebox.showerror("No Solution", "No solution exists for this maze.")
            return
        self.animate_solution(path)

    def animate_solution(self, path):
        """Animate the solution path."""
        self.start_time = time.time()
        self.animate_path(path, 0)

    def animate_path(self, path, index):
        """Move the character along the path."""
        if index < len(path):
            row, col = path[index]
            self.canvas.coords(self.character, col * self.cell_size + self.cell_size // 2,
                               row * self.cell_size + self.cell_size // 2)
            self.root.after(100, self.animate_path, path, index + 1)

    def reset_game(self):
        """Reset the game and maze."""
        self.maze = MazeGraph(self.maze.rows, self.maze.cols)
        self.generate_maze()
        self.canvas.delete("all")

    def randomize_maze(self):
        """Randomize the maze with new walls and start/end positions."""
        self.generate_maze()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Maze Solver Game")
    maze = MazeGraph(10, 10)  # Default maze size
    app = MazeSolverApp(root, maze)
    root.mainloop()
