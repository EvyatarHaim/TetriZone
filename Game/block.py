from Game.colors import Colors
import pygame
from Game.position import Position


# Represents a block in the Tetris game.
class Block:
    def __init__(self, shape_id: int):
        self.shape_id = shape_id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    # Moves the block by the specified number of rows and columns.
    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    # Returns the current positions of the block's cells, adjusted for the current offset.
    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    # Rotate the block.
    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    # Undo the rotation.
    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == -1:
            self.rotation_state = len(self.cells) - 1

    # Draw the block on the grid with the given offset.
    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size,
                                    offset_y + tile.row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.shape_id], tile_rect)
