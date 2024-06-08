import pygame
from Game.colors import Colors


class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    # Print the grin on the console - for testing.
    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end=" ")
            print()

    # Check if the shape is inside.
    def is_inside(self, row, column):
        if (row >= 0 and row < self.num_rows ) and (column >= 0 and column < self.num_cols):
            return True
        return False

    # Check if the cell is empty.
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    # Check if the row is full, if full we need to clear the row.
    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    # Clear the row.
    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    # Moving the row down by one, after the player break a line.
    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row + num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    # Clear al the full rows and return the number of rows that have been cleaned.
    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    # Reset the grid.
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    # Draw the grid.
    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column * self.cell_size + 11, row * self.cell_size + 11,
                                        self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
