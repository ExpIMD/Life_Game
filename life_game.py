import numpy as np
import tkinter as tk
from tkinter import colorchooser

class life_game:

    # Units of measurement - pixel
    WIDTH, HEIGHT = 900, 900

    CELL_SIZE = 10
    GRID_WIDTH = WIDTH // CELL_SIZE
    GRID_HEIGHT = HEIGHT // CELL_SIZE

    DIRECTIONS = [0, 1, -1]

    # Units of measurement - ms
    MAX_DELAY = 1000
    MIN_DELAY = 10
    STEP = 10

    MAX_AGE = 10

    def __init__(self, probability: tuple[float, float]):
        self._root = tk.Tk()

        self._grid = np.random.choice([0, 1], size=(life_game.GRID_WIDTH, life_game.GRID_HEIGHT), p=probability)
        self._delay: int = life_game.MAX_DELAY // 2
        self._is_paused: bool = False
        self._main_color: tuple[int, int, int] = (0, 255, 0) # By default, the cells are green
        self._background_color: str = "black" # By default, the background is black

        # Main window

        self._rectangles = [[None]*life_game.GRID_HEIGHT for _ in range(life_game.GRID_WIDTH)]
        self._canvas = tk.Canvas(self._root, width=life_game.WIDTH, height=life_game.HEIGHT, bg=self._background_color)

        for x in range(life_game.GRID_WIDTH):
            for y in range(life_game.GRID_HEIGHT):
                x1 = x * life_game.CELL_SIZE
                y1 = y * life_game.CELL_SIZE
                x2 = x1 + life_game.CELL_SIZE
                y2 = y1 + life_game.CELL_SIZE
                
                temp = self._canvas.create_rectangle(x1, y1, x2, y2, fill="black", width=0)
                self._rectangles[x][y] = temp
        self._canvas.pack()

        self._root.title("Life game")
        self._root.resizable(False, False)

        # Auxiliary window

        self._control = tk.Toplevel(self._root)
        self._control.title("Controls")
        self._control.geometry("200x250")
        self._control.resizable(False, False)

        self._control.transient(self._root)

        choose_color_button = tk.Button(self._control, text="Choose Cell Color", command=self.choose_cell_color)
        choose_color_button.pack(fill='x', padx=10, pady=5)

        choose_bg_button = tk.Button(self._control, text="Choose Background Color", command=self.choose_background_color)
        choose_bg_button.pack(fill='x', padx=10, pady=5)

        speed_up_button = tk.Button(self._control, text="Speed Up", command=self.speed_up)
        speed_up_button.pack(fill='x', padx=10, pady=5)

        slow_down_button = tk.Button(self._control, text="Slow Down", command=self.slow_down)
        slow_down_button.pack(fill='x', padx=10, pady=5)

        pause_button = tk.Button(self._control, text="Pause", command=self.pause)
        pause_button.pack(fill='x', padx=10, pady=5)

        self._delay_label = tk.Label(self._control, text=f"Delay: {self._delay} ms")
        self._delay_label.pack(pady=10)
    
    def run(self) -> None:
        """
        Description:
            Launching the window application with the Life game simulation
        """

        self.setting()
        self.update_grid()
        self._root.mainloop()

    def setting(self):
        """
        Description:
            Setting up control keys
        """

        self._root.bind("<space>", self.pause)
        self._root.bind("<Up>", self.slow_down)
        self._root.bind("<Down>", self.speed_up)
    
    def pause(self, event=None):
        self._is_paused = not self._is_paused
        self.update_delay_label()

    def update_delay_label(self):
        self._delay_label.config(text=f"Delay: {self._delay} ms")

    def speed_up(self, event=None):
        self._delay = max(life_game.MIN_DELAY, self._delay - life_game.STEP)
        self.update_delay_label()

    def choose_background_color(self, event=None):
        color_code = colorchooser.askcolor(title="Choose background color")
        if color_code[1] is not None:
            self._background_color = color_code[1]
            self._canvas.config(bg=self._background_color)
            self.draw_grid()

    def slow_down(self, event=None):
        self._delay = min(life_game.MAX_DELAY, self._delay + life_game.STEP)
        self.update_delay_label()

    def choose_cell_color(self, event=None):
        color_code = colorchooser.askcolor(title="Choose main color")
        if color_code[0] is not None:
            r, g, b = map(int, color_code[0])
            self._main_color = (r, g, b)

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
                        neighbor_count += 1 if self._grid[xx][yy] > 0 else 0
                if self._grid[x][y] > 0:
                    if neighbor_count < 2 or neighbor_count > 3:
                        new_grid[x][y] = 0
                    else:
                        new_grid[x][y] = min(new_grid[x][y] + 1, life_game.MAX_AGE) # Age increases
                else:
                    if neighbor_count == 3:
                        new_grid[x][y] = 1
                    else:
                        new_grid[x][y] = 0

        self._grid = new_grid

    def draw_grid(self):
        for x in range(life_game.GRID_WIDTH):
            for y in range(life_game.GRID_HEIGHT):
                if self._grid[x][y] > 0:
                    color = self.get_color(self._grid[x][y])
                    self._canvas.itemconfig(self._rectangles[x][y], fill=color)
                else:
                    self._canvas.itemconfig(self._rectangles[x][y], fill=self._background_color)
    
    def get_color(self, age: int):
        age = min(age, life_game.MAX_AGE)
        r, g, b = self._main_color
        factor = age / life_game.MAX_AGE
        r = int(r * (0.3 + 0.7 * factor))
        g = int(g * (0.3 + 0.7 * factor))
        b = int(b * (0.3 + 0.7 * factor))
        return f"#{r:02x}{g:02x}{b:02x}"


