# game.py

import random
from .cell import Cell  # Import the Cell class from cell.py

class Minesweeper:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self._place_mines()
        self._calculate_adjacent_mines()
        self.game_over = False
        self.cells_left = width * height - num_mines

    def _place_mines(self):
            # Randomly place mines
            all_cells = [cell for row in self.grid for cell in row]
            mines = random.sample(all_cells, self.num_mines)
            for mine in mines:
                mine.is_mine = True

    def _calculate_adjacent_mines(self):
        for row in self.grid:
            for cell in row:
                if not cell.is_mine:
                    cell.adjacent_mines = self._count_adjacent_mines(cell)

    def _count_adjacent_mines(self, cell):
        count = 0
        for neighbor in self.get_neighbors(cell):
            if neighbor.is_mine:
                count += 1
        return count

    def get_neighbors(self, cell):
        neighbors = []
        for y in range(max(0, cell.y - 1), min(self.height, cell.y + 2)):
            for x in range(max(0, cell.x - 1), min(self.width, cell.x + 2)):
                if (x, y) != (cell.x, cell.y):
                    neighbors.append(self.grid[y][x])
        return neighbors

    def reveal_cell(self, x, y):
        cell = self.grid[y][x]
        if cell.is_revealed or cell.is_flagged:
            return
        cell.is_revealed = True
        if cell.is_mine:
            self.game_over = True
            print("Boom! You hit a mine.")
        else:
            self.cells_left -= 1
            if cell.adjacent_mines == 0:
                for neighbor in self.get_neighbors(cell):
                    if not neighbor.is_revealed:
                        self.reveal_cell(neighbor.x, neighbor.y)

    def flag_cell(self, x, y):
        cell = self.grid[y][x]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged