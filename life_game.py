import numpy as np
import tkinter as tk

class life_game:

    WIDTH, HEIGHT = 1000, 1000
    CELL_SIZE = 10
    GRID_WIDTH = WIDTH // CELL_SIZE
    GRID_HEIGHT = HEIGHT // CELL_SIZE
    DIRECTIONS = [0, 1, -1]

    def __init__(self):
        self._root = tk.Tk()

        self._grid = np.random.choice([0, 1], size=(life_game.GRID_WIDTH, life_game.GRID_HEIGHT), p=[0.9, 0.1])
        self._delay: int = 100
        self._is_paused: bool = False

        self._rectangles = [[None]*life_game.GRID_HEIGHT for _ in range(life_game.GRID_WIDTH)]
        self._canvas = tk.Canvas(self._root, width=life_game.WIDTH, height=life_game.HEIGHT, bg="black")

        for x in range(life_game.GRID_WIDTH):
            for y in range(life_game.GRID_HEIGHT):
                x1 = x * life_game.CELL_SIZE
                y1 = y * life_game.CELL_SIZE
                x2 = x1 + life_game.CELL_SIZE
                y2 = y1 + life_game.CELL_SIZE
                
                temp = self._canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="")
                self._rectangles[x][y] = temp
        self._canvas.pack()

        self._root.title("Life game")
    
    def run(self):
        self.setting()
        self.update_grid()
        self._root.mainloop()

    def setting(self):
        self._root.bind("<space>", self.pause)

    def pause(self, event=None):
        self._is_paused = not self._is_paused
        pass

    def update_grid(self):
        if not self._is_paused:
            self.update_state()
            self.draw_grid()
        self._root.after(self._delay, self.update_grid)

    def update_state(self):
        new_grid = np.copy(self._grid)
        for x in range(life_game.GRID_WIDTH):
            for y in range(life_game.GRID_HEIGHT):
                neighbor_count = 0
                for dx in life_game.DIRECTIONS:
                    for dy in life_game.DIRECTIONS:
                        if dx == 0 and dy == 0:
                            continue
                        xx, yy = (x + dx) % life_game.GRID_WIDTH, (y + dy) % life_game.GRID_HEIGHT
                        neighbor_count += self._grid[xx][yy]
                if self._grid[x][y] == 1:
                    if neighbor_count < 2 or neighbor_count > 3:
                        new_grid[x][y] = 0
                else:
                    if neighbor_count == 3:
                        new_grid[x][y] = 1
        self._grid = new_grid


    def draw_grid(self):
        for x in range(life_game.GRID_WIDTH):
            for y in range(life_game.GRID_HEIGHT):
                if self._grid[x][y] == 1:
                    self._canvas.itemconfig(self._rectangles[x][y], fill="green")
                else:
                    self._canvas.itemconfig(self._rectangles[x][y], fill="black")

