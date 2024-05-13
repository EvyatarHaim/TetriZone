from Game.grid import Grid
from Game.shape import *
import random
import pygame


class Game:
    def __init__(self):
        self.grid = Grid()
        self.shapes = [IShape(), JShape(), LShape(), OShape(), SShape(), TShape(), ZShape()]
        self.current_shape = self.get_random_shape()
        self.next_shape = self.get_random_shape()
        self.game_over = False
        self.score = 0
        self.lines = 0
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

        pygame.mixer.music.load("Sounds/music.ogg")
        pygame.mixer.music.play(-1)

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points

    def get_random_shape(self):
        if len(self.shapes) == 0:
            self.shapes = [IShape(), JShape(), LShape(), OShape(), SShape(), TShape(), ZShape()]
        random_shape = random.choice(self.shapes)
        self.shapes.remove(random_shape)
        return random_shape

    def move_left(self):
        self.current_shape.move(0, -1)
        if not self.shape_inside() or not self.shape_fits():
            self.current_shape.move(0, 1)

    def move_right(self):
        self.current_shape.move(0, 1)
        if not self.shape_inside() or not self.shape_fits():
            self.current_shape.move(0, -1)

    def move_down(self):
        self.current_shape.move(1, 0)
        if self.shape_inside() == False or self.shape_fits() == False:
            self.current_shape.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_shape.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_shape.shape_id
        self.current_shape = self.next_shape
        self.next_shape = self.get_random_shape()
        rows_cleared = self.grid.clear_full_rows()
        self.lines += rows_cleared
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if not self.shape_fits():
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.shapes = [IShape(), JShape(), LShape(), OShape(), SShape(), TShape(), ZShape()]
        self.current_shape = self.get_random_shape()
        self.next_shape = self.get_random_shape()
        self.score = 0

    def shape_fits(self):
        tiles = self.current_shape.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_shape.rotate()
        if self.shape_inside() == False or self.shape_fits() == False:
            self.current_shape.undo_rotation()
        else:
            self.rotate_sound.play()

    def shape_inside(self):
        tiles = self.current_shape.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_shape.draw(screen, 11, 11)

        if self.next_shape.shape_id == 3:
            self.next_shape.draw(screen, 255, 290)
        elif self.next_shape.shape_id == 4:
            self.next_shape.draw(screen, 255, 280)
        else:
            self.next_shape.draw(screen, 270, 270)

    def get_lines(self):
        return self.lines
