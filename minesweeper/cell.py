class Cell:
    def __init__(self, x, y):
        self.x = x  # X position on the grid
        self.y = y  # Y position on the grid
        self.is_mine = False  # Whether the cell is a mine
        self.is_revealed = False  # Whether the cell has been revealed
        self.is_flagged = False  # Whether the cell has been flagged
        self.adjacent_mines = 0  # Number of adjacent mines
