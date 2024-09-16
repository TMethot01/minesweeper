# main.py

import tkinter as tk
from minesweeper.gui import MinesweeperGUI  # Import the GUI class
from minesweeper.settings import GameSettings

if __name__ == "__main__":
    root = tk.Tk()
    settings = GameSettings('expert') # difficulties are beginner, intermediate, and expert.
    gui = MinesweeperGUI(root, width=settings.width, height=settings.height, mines=settings.mines)
    root.mainloop()
