#!/usr/bin/env python3


import random
import typing

class TetrisState():
    """Tetris states are all the same really
    - it's a driver TetrisGame that differentiates gametypes
    """
    def __init__(self, block_grid: 'BlockGrid', piece: 'Piece'):
        self.block_grid = BlockGrid()
        self.current_piece = piece

class Piece():
    """A collection of blocks"""
    pass



class Block():
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        if self.label == "empty":
            return " "
        else:
            return "x"


class BlockGrid():

    def __init__(self, x_dimension=10, y_dimension=20, cheese_count=0):
        if cheese_count > y_dimension:
            raise RuntimeError
        self.grid = []

        for y in range(y_dimension):
            self.grid.append([Block("empty")] * x_dimension)

        for cheese_y in range(cheese_count):
            cheese_row = [Block("cheese")] * x_dimension
            hole_index = random.choice(range(x_dimension))
            cheese_row[hole_index] = Block("empty")
            self.grid[y_dimension - cheese_y - 1] = cheese_row

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
