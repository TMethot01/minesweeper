import tkinter as tk
from tkinter import messagebox
from .game import Minesweeper

flag_list = []
bomb_list = []

class MinesweeperGUI:
    def __init__(self, master, width=9, height=9, mines=10):
        self.master = master
        self.master.title("Minesweeper")
        self.game = Minesweeper(width, height, mines)
        self.buttons = [[None for _ in range(width)] for _ in range(height)]
        self.create_widgets()
        self.left_button_pressed = False
        self.right_button_pressed = False
        self.mine_counter = self.game.num_mines
        self.counter_label = tk.Label(self.master, text=f"Mines: {self.mine_counter}")
        self.counter_label.grid(row=0, column=0, columnspan=self.game.width)
        self.flag_image = tk.PhotoImage(file="assets/flag2.png", width=20, height=20)
        flag_list.append(self.flag_image)
        self.bomb_image = tk.PhotoImage(file="assets/bomb2.png", width=20, height=20)
        bomb_list.append(self.bomb_image)


    def create_widgets(self):
        for y in range(self.game.height):
            for x in range(self.game.width):
                button = tk.Button(self.master, width=2, height=1)
                button.grid(row=y+1, column=x)  # Adjust row if needed

                # Bind left button events
                button.bind('<ButtonPress-1>', lambda event, x=x, y=y: self.on_left_button_press(event, x, y))
                button.bind('<ButtonRelease-1>', lambda event, x=x, y=y: self.on_left_button_release(event, x, y))

                # Bind right button events
                button.bind('<ButtonPress-3>', lambda event, x=x, y=y: self.on_right_button_press(event, x, y))
                button.bind('<ButtonRelease-3>', lambda event, x=x, y=y: self.on_right_button_release(event, x, y))

                self.buttons[y][x] = button

    def check_for_chord(self, x, y):
        if self.left_button_pressed and self.right_button_pressed:
            cell = self.game.grid[x][y]
            if cell.is_revealed:
                flagged_neighbors = sum(1 for neighbor in self.game.get_neighbors(cell) if neighbor.is_flagged)
                if flagged_neighbors == cell.adjecent_mines:
                    for neighbor in self.game.get_neighbors(cell):
                        if not neighbor.is_flagged and not neighbor.is_revealed:
                            self.game.reveal_cell(neighbor.x, neighbor.y)
                            self.update_button(neighbor.x, neighbor.y)

    def on_left_button_press(self, event, x, y):
        self.left_button_pressed = True
        self.check_for_chord(x, y)

    def on_left_button_release(self, event, x, y):
        self.left_button_pressed = False
        if self.game.game_over:
            return
        cell = self.game.grid[y][x]
        if cell.is_flagged:
            return
        self.game.reveal_cell(x, y)
        self.update_button(x, y)
        if self.game.game_over:
            self.reveal_all_mines()
            messagebox.showinfo("Game Over", "You hit a mine!")
        elif self.game.cells_left == 0:
            self.reveal_all_mines()
            messagebox.showinfo("Congratulations", "You won!")

    def on_right_button_press(self, event, x, y):
        self.right_button_pressed = True
        self.check_for_chord(x, y)

    def on_right_button_release(self, event, x, y):
        self.right_button_pressed = False
        if self.game.game_over:
            return
        self.game.flag_cell(x, y)
        self.update_button(x, y)

    def update_button(self, x, y):
        cell = self.game.grid[y][x]
        button = self.buttons[y][x]
        if cell.is_revealed:
            if cell.is_mine:
                button.config(image=self.bomb_image)
            else:
                button.config(text=str(cell.adjacent_mines) if cell.adjacent_mines > 0 else '', bg="light grey", relief=tk.SUNKEN)
        elif cell.is_flagged:
            button.config(image=self.flag_image, width=18, height=18)
        else:
            button.config(text='', bg="SystemButtonFace")

    def reveal_all_mines(self):
        for y in range(self.game.height):
            for x in range(self.game.width):
                cell = self.game.grid[y][x]
                if cell.is_mine:
                    button = self.buttons[y][x]
                    button.config(image=self.bomb_image)