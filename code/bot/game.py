#!/usr/bin/env python3

import random, copy

T_PIECE = ((0, -1, "b"), (-1, 0, "b"), (0, 0, "b"), (1, 0, "b"))
L_PIECE = ((0, 0, "b"), (1, 0, "b"), (0, -1, "b"), (0, -2, "b"))
J_PIECE = ((0, 0, "b"), (-1, 0, "b"), (0, -1, "b"), (0, -2, "b"))
O_PIECE = ((0, 0, "b"), (1, 0, "b"), (0, -1, "b"), (1, -1, "b"))
S_PIECE = ((0, 0, "b"), (-1, 0, "b"), (0, -1, "b"), (1, -1, "b"))
Z_PIECE = ((0, 0, "b"), (-1, 0, "b"), (0, -1, "b"), (1, -1, "b"))
I_PIECE = ((0, 0, "b"), (0, -1, "b"), (0, -2, "b"), (0, -3, "b"))

PIECES = [T_PIECE, L_PIECE, J_PIECE, O_PIECE, S_PIECE, Z_PIECE, I_PIECE]
# TODO set up gamestate/successor

BLANK_LABEL = "_"
CHEESE_LABEL = "c"


class TetrisGame:
    """Generic game"""


class TetrisState:
    """Generic state"""

    pass


def new_cheese_state(
    x_dimension=10, y_dimension=20, hole_count=1, cheese_count=9, piece=None
):
    if piece is None:
        piece = random.choice(PIECES)
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
    spawn = (x_dimension // 2, 0)
    mapped_piece = shift_piece(piece, spawn[0], spawn[1])

    return CheeseState(spawn, spawn, mapped_piece, grid)


def shift_piece(piece, x_shift, y_shift):
    """Shift every coordinate in piece"""
    new_piece = []
    for i in range(len(piece)):
        x, y, label = piece[i]
        new_brick = (x + x_shift, y + y_shift, label)
        new_piece.append(new_brick)
    return tuple(new_piece)


class CheeseGame:
    """Clear all the cheese to win."""

    pass


class Randomizer:
    pass


class SimpleRandomizer(Randomizer):
    def __init__(self, bag, weights=None):
        self.bag = bag

    def choice(self):
        return random.choice(self.bag)


class CheeseState(TetrisState):
    """CheeseState- may be illegal"""

    def __init__(self, spawn, anchor, piece, grid):
        self.spawn = spawn  # one position
        self.anchor = anchor  # one position
        self.piece = piece  # list of positions
        self.grid = grid  # list of list of one-char strings

    def move_anchor(self, x_shift, y_shift):
        """Return a new state with moved anchor and piece."""
        anchor_x, anchor_y = self.anchor
        # tuple addition?
        new_anchor = (anchor_x + x_shift, anchor_y + y_shift)
        new_piece = shift_piece(self.piece, x_shift, y_shift)
        return CheeseState(self.spawn, new_anchor, new_piece, self.grid)

    def is_legal(self):
        """Illegal if oob or intersecting"""
        for i in range(len(self.piece)):
            x, y, label = self.piece[i]
            if x < 0 or x >= len(self.grid[0]) or y < 0 or grid[y][x] != BLANK_LABEL:
                return False
        return True

    def lock_piece(self, randomizer):
        """Fix the current piece to the board if possible, and get a new one"""

    def __repr__(self):
        rep = []
        st = ""

        for row in self.grid:
            rep.append(list(row))
        for i in range(len(self.piece)):
            x, y, label = self.piece[i]
            if x in range(len(self.grid[0])) and y in range(len(self.grid)):
                rep[y][x] = label
        count = 0
        for row in rep:
            for block in row:
                st += block
            st += f" {count}\n"
            count += 1
        return st

    def rotate_left(self):
        new_piece = []
        anchor_x, anchor_y = self.anchor
        for i in range(len(self.piece)):
            x, y, label = self.piece[i]
            offset_x, offset_y = (x - anchor_x, y - anchor_y)
            new_offset_x, new_offset_y = (offset_y, -1 * offset_x)
            new_x, new_y = (new_offset_x + anchor_x, new_offset_y + anchor_y)
            new_piece.append((new_x, new_y, label))
        new_piece = tuple(new_piece)
        return CheeseState(self.spawn, self.anchor, new_piece, self.grid)

    def rotate_right(self):
        new_piece = []
        anchor_x, anchor_y = self.anchor
        for i in range(len(self.piece)):
            x, y, label = self.piece[i]
            offset_x, offset_y = (x - anchor_x, y - anchor_y)
            new_offset_x, new_offset_y = (-1 * offset_y, offset_x)
            new_x, new_y = (new_offset_x + anchor_x, new_offset_y + anchor_y)
            new_piece.append((new_x, new_y, label))
        new_piece = tuple(new_piece)
        return CheeseState(self.spawn, self.anchor, new_piece, self.grid)


# def send_garbage(state, garbage_label, garbage_count, hole_count):
#     piece, grid = state

#     new_grid = []
#     for i in range(len(grid) - garbage_count):
#         new_grid.append(grid[i + garbage_count])

#     for g in range(len(grid) - garbage_count, len(grid)):
#         to_hole = hole_count
#         garbage_row = garbage_label * len(grid[0])

#         while to_hole != 0:
#             hole_index = random.choice(range(len(grid[0])))
#             garbage_row = garbage_row[:hole_index] + " " + garbage_row[hole_index:-1]
#             to_hole -= 1
#         new_grid.append(garbage_row)
#     new_state = (piece, tuple(new_grid))
#     return (piece, tuple(new_grid))
