#!/usr/bin/env python3


import random
import typing
import unittest

class TetrisGame():
    """Our search-problem class"""

    def __init__(self):
        pass

    def add_piece(self):
        """Add a specific piece to the game"""
        pass

    def next_piece(self):
        pass

    def is_terminal(self, state: 'TetrisState'):
        """Can be re-implemented based on subclass of game"""
        # Default: there exists a block greater than the "roof"
        pass

    def get_succs(self):
        pass

class TetrisState():
    """Tetris states are all the same really
    - it's a driver TetrisGame that differentiates gametypes
    """
    def __init__(self, block_grid: 'BlockGrid', piece: 'Piece'):
        self.block_grid = BlockGrid()
        self.current_piece = piece

class Piece():
    """A collection of blocks- limited to 5x5
    Pieces rotate about the center at (2, 2) - sculpt accordingly
    """

    def __init__(self, block_label: str, block_coordinates: list):
        self.piece_grid = []
        for i in range(5):
            self.piece_grid.append([Block("empty")] * 5)
        for x, y in block_coordinates:
            self.piece_grid[x][y] = Block(block_label)

    def left_rotate(self):
        for y in range(len(self.piece_grid)):
            for x in range(len(self.piece_grid[0])):
                if x == 2 and y == 2:
                    # can't rotate the center this way- but the center never changes anyway
                    continue
                offset_x, offset_y = (x - 2, y - 2)
                new_offset_x, new_offset_y = (offset_y, -1 * offset_x)
                new_x, new_y = (new_offset_x + 2, new_offset_y + 2)
                self.piece_grid[new_y][new_x] = self.piece_grid[y][x]


class Block():
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        if self.label == "empty":
            return " "
        else:
            return "x"

    def __eq__(self, o):
        return self.label == o.label


class BlockGrid():

    def __init__(self, x_dimension=10, y_dimension=20):
        self.grid = []
        self.x_dimension = x_dimension
        self.y_dimension = y_dimension

        for y in range(y_dimension):
            self.grid.append([Block("empty")] * x_dimension)

    def send_garbage(self, garbage_count: int, garbage_label: str, hole_count: int):
        if hole_count > self.x_dimension:
            raise RuntimeError
        for garbage_y in range(garbage_count):
            garbage_row = [Block(garbage_label)] * self.x_dimension
            while hole_count != 0:
                new_hole_index = random.choice(range(self.x_dimension))
                if garbage_row[new_hole_index] != Block("empty"):
                    garbage_row[new_hole_index] = Block("empty")
                    hole_count -= 1
            self.grid[self.y_dimension - garbage_y -1] = garbage_row

    def __repr__(self):
        repr = ""
        for row in self.grid:
            repr += "|"
            for block in row:
                repr += block.__repr__()
            repr += "|\n"
        return repr

def main():
    print("foobar")


if __name__ == "__main__":
    main()
