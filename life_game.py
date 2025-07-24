import numpy as np
import tkinter as tk
from tkinter import colorchooser
import time

class life_game:
    """
    Description:
        Implementation of Conway's Game of Life simulation with a graphical interface using Tkinter.

        The game consists of a grid of cells, each of which can be alive or dead. The simulation evolves
        in discrete time steps according to the following rules:
            1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
            2. Any live cell with two or three live neighbors lives on to the next generation.
            3. Any live cell with more than three live neighbors dies, as if by overpopulation.
            4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

        Each cell tracks its "age" (how many generations it has been alive), influencing its color intensity.
        Users can control simulation speed, pause/resume, and pick colors for cells and background.
    """

    # Units of measurement - pixel

    WIDTH, HEIGHT = 700, 500

    CELL_SIZE: int = 10
    GRID_WIDTH: int = WIDTH // CELL_SIZE
    GRID_HEIGHT: int = HEIGHT // CELL_SIZE

    DIRECTIONS: list[int] = [0, 1, -1]

    # Units of measurement - ms

    MAX_DELAY: int = 1000
    MIN_DELAY: int = 10
    STEP: int = 10

    MAX_AGE: int = 10

    def __init__(self, probability: tuple[float, float]):
        self._root = tk.Tk()

        self._grid = np.random.choice([0, 1], size=(life_game.GRID_HEIGHT, life_game.GRID_WIDTH), p=probability)
        self._delay: int = life_game.MAX_DELAY // 2
        self._is_paused: bool = False

        self._last_update_timer: float = time.time() # Units of measurement - s
        self._timer: float = 0.0

        self._cell_color: tuple[int, int, int] = (0, 255, 0) # By default, the cells are green
        self._background_color: str = "black" # By default, the background is black

        # Main window

        self._root.title("Life game")
        self._root.resizable(False, False)

        self._rectangles = [[None]*life_game.GRID_WIDTH for _ in range(life_game.GRID_HEIGHT)]
        self._canvas = tk.Canvas(self._root, width=life_game.WIDTH, height=life_game.HEIGHT, bg=self._background_color)

        for i in range(life_game.GRID_HEIGHT):
            for j in range(life_game.GRID_WIDTH):
                i1 = i * life_game.CELL_SIZE
                j1 = j * life_game.CELL_SIZE
                i2 = i1 + life_game.CELL_SIZE
                j2 = j1 + life_game.CELL_SIZE
                
                self._rectangles[i][j] = self._canvas.create_rectangle(i1, j1, i2, j2, fill=self._background_color, width=0)
        self._canvas.pack()

        # Auxiliary window

        self._control_window = tk.Toplevel(self._root)
        self._control_window.title("Controls")
        self._control_window.geometry("200x350")
        self._control_window.resizable(False, False)

        self._control_window.transient(self._root)
        self._control_window.protocol("WM_DELETE_WINDOW", self._on_control_window_close)

        choose_color_button = tk.Button(self._control_window, text="Choose Cell Color", command=self.choose_cell_color)
        choose_color_button.pack(fill='x', padx=10, pady=5)

        choose_bg_button = tk.Button(self._control_window, text="Choose Background Color", command=self.choose_background_color)
        choose_bg_button.pack(fill='x', padx=10, pady=5)

        speed_up_button = tk.Button(self._control_window, text="Speed Up", command=self.speed_up)
        speed_up_button.pack(fill='x', padx=10, pady=5)

        slow_down_button = tk.Button(self._control_window, text="Slow Down", command=self.slow_down)
        slow_down_button.pack(fill='x', padx=10, pady=5)

        pause_button = tk.Button(self._control_window, text="Pause", command=self.pause)
        pause_button.pack(fill='x', padx=10, pady=5)

        self._population_label = tk.Label(self._control_window, text="Population: 0")
        self._population_label.pack(pady=5)

        self._timer_label = tk.Label(self._control_window, text="Simulation time: 0 s")
        self._timer_label.pack(pady=5)

        self._delay_label = tk.Label(self._control_window, text=f"Delay: {self._delay} ms")
        self._delay_label.pack(pady=10)
    
    def run(self) -> None:
        """
        Description:
            Launching the window application with the Life game simulation
        """

        self.setting()
        self.update_simmulation_state()
        self._root.mainloop()

    def setting(self) -> None:
        """
        Description:
            Setting up control keys
        """

        self._root.bind_all("<space>", self.pause)
        self._root.bind_all("<Up>", self.slow_down)
        self._root.bind_all("<Down>", self.speed_up)
        self._root.bind_all("<Escape>", self.toggle_control_window)

    def _on_control_window_close(self):
        self._control_window.withdraw()

    def pause(self, event=None) -> None:
        """
        Description:
            Controlling the simulation pause
        """

        self._is_paused = not self._is_paused
        self.update_delay_label()

    def update_delay_label(self) -> None:
        """
        Description:
            Updating the delay label
        """

        self._delay_label.config(text=f"Delay: {self._delay} ms")

    def speed_up(self, event=None) -> None:
        """
        Description:
            Speeding up the simulation
        """

        self._delay = max(life_game.MIN_DELAY, self._delay - life_game.STEP)
        self.update_delay_label()

    def choose_background_color(self, event=None) -> None:
        """
        Description:
            Slowing down the simulation
        """

        color_code = colorchooser.askcolor(title="Choose background color")
        if color_code[1] is not None:
            self._background_color = color_code[1]
            self._canvas.config(bg=self._background_color)
            self.draw_grid()

    def slow_down(self, event=None) -> None:
        """
        Description:
            Choosing the background color
        """

        self._delay = min(life_game.MAX_DELAY, self._delay + life_game.STEP)
        self.update_delay_label()

    def choose_cell_color(self, event=None) -> None:
        """
        Description:
            Choosing the main color for cells
        """

        color_code = colorchooser.askcolor(title="Choose the main color for cells")
        if color_code[0] is not None:
            r, g, b = map(int, color_code[0])
            self._cell_color = (r, g, b)

    def update_simmulation_state(self) -> None:
        """
        Description:
            Updating the simulation state
        """

        if not self._is_paused:
            self.update_grid()
            self.draw_grid()

            now = time.time()
            self._timer += now - self._last_update_timer
            self._last_update_timer = now

        population = np.count_nonzero(self._grid) # It is better to perform one operation than to store the population size in one field and constantly increase or decrease it
        self._population_label.config(text=f"Population: {population}")

        self._timer_label.config(text=f"Simulation time: {int(self._timer)} s")

        self._root.after(self._delay, self.update_simmulation_state)

    def update_grid(self) -> None:
        """
        Description:
            Updating the grid storing cell ages.

            If a cell is dead, its age is 0. Otherwise, it is greater than or equal to 1.

            Rules based on neighbor counts:
            1. A live cell with fewer than two live neighbors dies.
            2. A live cell with two or three live neighbors continues to live.
            3. A live cell with more than three live neighbors dies.
            4. A dead cell with exactly three living neighbors becomes alive.
        """
                
        new_grid = np.copy(self._grid)

        for i in range(life_game.GRID_HEIGHT):
            for j in range(life_game.GRID_WIDTH):
                neighbor_count = 0
                for di in life_game.DIRECTIONS:
                    for dj in life_game.DIRECTIONS:
                        if di == 0 and dj == 0:
                            continue
                        ii, jj = (i + di) % life_game.GRID_HEIGHT, (j + dj) % life_game.GRID_WIDTH # Circular mesh
                        neighbor_count += 1 if self._grid[ii][jj] > 0 else 0
                if self._grid[i][j] > 0:
                    if neighbor_count < 2 or neighbor_count > 3:
                        new_grid[i][j] = 0
                    else:
                        new_grid[i][j] = min(new_grid[i][j] + 1, life_game.MAX_AGE) # Age increases
                else:
                    if neighbor_count == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0

        self._grid = new_grid

    def draw_grid(self) -> None:
        """
        Description:
            Drawing the grid in the window application
        """

        for i in range(life_game.GRID_HEIGHT):
            for j in range(life_game.GRID_WIDTH):
                if self._grid[i][j] > 0:
                    color = self.age_to_color(self._grid[i][j])
                    self._canvas.itemconfig(self._rectangles[i][j], fill=color)
                else:
                    self._canvas.itemconfig(self._rectangles[i][j], fill=self._background_color)
    
    def toggle_control_window(self, event=None) -> None:
        """
        Description:
            Toggle visibility of the control window when Escape is pressed.
        """
        
        if self._control_window.state() == 'withdrawn':
            self._control_window.deiconify()
            self._control_window.lift()  # Поднять окно поверх других
        else:
            self._control_window.withdraw()

    
    def age_to_color(self, age: int) -> str:
        """
        Description:
            Getting the color from the cell's age
        """

        age: int = min(age, life_game.MAX_AGE)
        factor: float = age / life_game.MAX_AGE

        r, g, b = self._cell_color
        r: int = int(r * (0.3 + 0.7 * factor))
        g: int = int(g * (0.3 + 0.7 * factor))
        b: int = int(b * (0.3 + 0.7 * factor))

        return f"#{r:02x}{g:02x}{b:02x}"