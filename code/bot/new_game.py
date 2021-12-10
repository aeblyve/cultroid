#!/usr/bin/env python3
import random, copy
from enum import Enum

# TODO: Investigate "enumerable pieces" approach

BLANK_LABEL = "_"
CHEESE_LABEL = "c"


class TetrisPiece(Enum):
    T_PIECE = (1,)
    L_PIECE = (2,)
    J_PIECE = (3,)
    O_PIECE = (4,)
    S_PIECE = (5,)
    Z_PIECE = (6,)
    I_PIECE = 7


CONFIGURATIONS = {}

# TODO: order these so that the first point is always bottom-most
CONFIGURATIONS[TetrisPiece.T_PIECE] = [
    ((0, -1, "b"), (-1, 0, "b"), (0, 0, "b"), (1, 0, "b")),
    ((-1, 0, "b"), (0, 1, "b"), (0, 0, "b"), (0, -1, "b")),
    ((0, 1, "b"), (1, 0, "b"), (0, 0, "b"), (-1, 0, "b")),
    ((1, 0, "b"), (0, -1, "b"), (0, 0, "b"), (0, 1, "b")),
]
CONFIGURATIONS[TetrisPiece.L_PIECE] = [
    ((0, 0, "b"), (1, 0, "b"), (0, -1, "b"), (0, -2, "b")),
    ((0, 0, "b"), (0, -1, "b"), (-1, 0, "b"), (-2, 0, "b")),
    ((0, 0, "b"), (-1, 0, "b"), (0, 1, "b"), (0, 2, "b")),
    ((0, 0, "b"), (0, 1, "b"), (1, 0, "b"), (2, 0, "b")),
]
CONFIGURATIONS[TetrisPiece.J_PIECE] = [
    ((0, 0, "b"), (-1, 0, "b"), (0, -1, "b"), (0, -2, "b")),
    ((0, 0, "b"), (0, 1, "b"), (-1, 0, "b"), (-2, 0, "b")),
    ((0, 0, "b"), (1, 0, "b"), (0, 1, "b"), (0, 2, "b")),
    ((0, 0, "b"), (0, -1, "b"), (1, 0, "b"), (2, 0, "b")),
]
CONFIGURATIONS[TetrisPiece.O_PIECE] = [
    ((0, 0, "b"), (1, 0, "b"), (0, -1, "b"), (1, -1, "b")),
    ((0, 0, "b"), (0, -1, "b"), (-1, 0, "b"), (-1, -1, "b")),
    ((0, 0, "b"), (-1, 0, "b"), (0, 1, "b"), (-1, 1, "b")),
    ((0, 0, "b"), (0, 1, "b"), (1, 0, "b"), (1, 1, "b")),
]
CONFIGURATIONS[TetrisPiece.S_PIECE] = [
    ((0, 0, "b"), (-1, 0, "b"), (0, -1, "b"), (1, -1, "b")),
    ((0, 0, "b"), (0, 1, "b"), (-1, 0, "b"), (-1, -1, "b")),
    ((0, 0, "b"), (1, 0, "b"), (0, 1, "b"), (-1, 1, "b")),
    ((0, 0, "b"), (0, -1, "b"), (1, 0, "b"), (1, 1, "b")),
]
CONFIGURATIONS[TetrisPiece.Z_PIECE] = [
    ((0, 0, "b"), (-1, 0, "b"), (0, -1, "b"), (1, -1, "b")),
    ((0, 0, "b"), (0, 1, "b"), (-1, 0, "b"), (-1, -1, "b")),
    ((0, 0, "b"), (1, 0, "b"), (0, 1, "b"), (-1, 1, "b")),
    ((0, 0, "b"), (0, -1, "b"), (1, 0, "b"), (1, 1, "b")),
]
CONFIGURATIONS[TetrisPiece.I_PIECE] = [
    ((0, 0, "b"), (0, -1, "b"), (0, -2, "b"), (0, -3, "b")),
    ((0, 0, "b"), (-1, 0, "b"), (-2, 0, "b"), (-3, 0, "b")),
    ((0, 0, "b"), (0, 1, "b"), (0, 2, "b"), (0, 3, "b")),
    ((0, 0, "b"), (1, 0, "b"), (2, 0, "b"), (3, 0, "b")),
]


class SimpleRandomizer(Randomizer):
    def __init__(self, bag, weights=None):
        self.bag = bag

    def choice(self):
        return random.choice(self.bag)


def new_cheese_state(
    y_dimension, x_dimension, hole_count=1, cheese_count=9, piece=None
):
    if piece is None:
        piece = random.choice(list(TetrisPiece))
    grid = []
    for y in range(y_dimension):
        row = [BLANK_LABEL] * x_dimension
        grid.append(tuple(row))

    for g in range(y_dimension - cheese_count, len(grid)):
        to_hole = hole_count
        cheese_row = [CHEESE_LABEL] * x_dimension

        while to_hole != 0:
            hole_index = random.choice(range(x_dimension))
            cheese_row[hole_index] = BLANK_LABEL
            to_hole -= 1
        grid[g] = tuple(cheese_row)

    grid = tuple(grid)
    return CheeseState(piece, grid)


def shift_piece(piece, x_shift, y_shift):
    """Shift every coordinate in piece"""
    new_piece = []
    for i in range(len(piece)):
        x, y, label = piece[i]
        new_brick = (x + x_shift, y + y_shift, label)
        new_piece.append(new_brick)
    return tuple(new_piece)


class CheeseState:
    def __init__(self, piece, grid):
        self.piece = piece
        self.grid = grid

    def num_cheese(self):
        return len(list(filter(lambda x: CHEESE_LABEL in x, self.grid)))

    def is_clear(self):
        """If the last row is clear, the whole stage is"""
        return self.grid[len(self.grid) - 1][0] != CHEESE_LABEL

    def __repr__(self):
        # TODO delet ref to piece
        rep = []
        st = ""

        for row in self.grid:
            rep.append(list(row))
        for x, y, label in self.piece:
            if x in range(len(self.grid[0])) and y in range(len(self.grid)):
                rep[y][x] = label
        count = 0
        for row in rep:
            for block in row:
                st += block
            st += f" {count}\n"
            count += 1
        return st

    def __hash__(self):
        return hash((self.piece, self.grid))

    def __eq__(self, other):
        if isinstance(other, CheeseState):
            return (other.piece == self.piece) and (other.grid == self.grid)

    def drill(self):
        # TODO this could be heuristic-optimized, most tetris games have a more or less linear top contour
        """Obtains y-indices where the top contour is defined"""
        points = []
        for i in range(len(self.grid[0])):
            ind = len(self.grid) - 1
            for j in range(len(self.grid)):
                if self.grid[j][i] != BLANK_LABEL:
                    ind = j
                    break
            points.append(ind)
        return points

    def get_top_contour(self):
        depth = max(self.drill())
        pass

    def enumerate_new_grids(self):
        # TODO: slide piece along "top contour"
        points = self.drill()
        grids = []
        for rot_piece in CONFIGURATIONS[self.piece]:
            for i in range(len(self.grid[0])):
                join_point = points[i] - 1
