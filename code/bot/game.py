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
#

BLANK_LABEL = "_"
CHEESE_LABEL = "c"


class TetrisState:
    """Generic state"""

    pass


def new_cheese_state(
    x_dimension=10, y_dimension=20, hole_count=1, cheese_count=9, piece=None
):
    # TODO init garbage - 9 rows of 1 hole

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

    return CheeseState(spawn, mapped_piece, grid)

    # piece, grid = state

    # new_grid = []
    # for i in range(len(grid) - garbage_count):
    #     new_grid.append(grid[i + garbage_count])

    # for g in range(len(grid) - garbage_count, len(grid)):
    #     to_hole = hole_count
    #     garbage_row = garbage_label * len(grid[0])

    #     while to_hole != 0:
    #         hole_index = random.choice(range(len(grid[0])))
    #         garbage_row = garbage_row[:hole_index] + " " + garbage_row[hole_index:-1]
    #         to_hole -= 1
    #     new_grid.append(garbage_row)
    # new_state = (piece, tuple(new_grid))
    # return (piece, tuple(new_grid))


def shift_piece(piece, x_shift, y_shift):
    """Shift every coordinate in piece"""
    new_piece = []
    for i in range(len(piece)):
        x, y, label = piece[i]
        new_brick = (x + x_shift, y + y_shift, label)
        new_piece.append(new_brick)
    return tuple(new_piece)


class CheeseState:
    """CheeseState- may be illegal"""

    def __init__(self, anchor, piece, grid):
        self.anchor = anchor  # one position
        self.piece = piece  # list of positions
        self.grid = grid  # list of list of one-char strings

    def move_anchor(self, x_shift, y_shift):
        """Return a new state with moved anchor and piece."""
        anchor_x, anchor_y = self.anchor
        # tuple addition?
        new_anchor = (anchor_x + x_shift, anchor_y + y_shift)
        new_piece = shift_piece(self.piece, x_shift, y_shift)
        return CheeseState(new_anchor, new_piece, self.grid)

    def is_legal(self):
        """Illegal if oob or intersecting"""
        for i in range(len(self.piece)):
            x, y, label = self.piece[i]
            if x < 0 or x >= len(self.grid[0]) or y < 0 or grid[y][x] != BLANK_LABEL:
                return False
        return True

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


def send_garbage(state, garbage_label, garbage_count, hole_count):
    piece, grid = state

    new_grid = []
    for i in range(len(grid) - garbage_count):
        new_grid.append(grid[i + garbage_count])

    for g in range(len(grid) - garbage_count, len(grid)):
        to_hole = hole_count
        garbage_row = garbage_label * len(grid[0])

        while to_hole != 0:
            hole_index = random.choice(range(len(grid[0])))
            garbage_row = garbage_row[:hole_index] + " " + garbage_row[hole_index:-1]
            to_hole -= 1
        new_grid.append(garbage_row)
    new_state = (piece, tuple(new_grid))
    return (piece, tuple(new_grid))


def generate_state(x_dimension=10, y_dimension=20):
    piece = random.choice(PIECES)
    new_center = (x_dimension // 2, 0)
    piece = recenter_piece(piece, new_center)
    grid = []
    for y in range(y_dimension):
        grid.append(" " * x_dimension)
    return (piece, tuple(grid))


def recenter_piece(piece, new_center):
    new_center_x, new_center_y = new_center
    old_center_x, old_center_y = piece[0]
    new_piece = [new_center]
    for i in range(1, len(piece)):
        x, y, label = piece[i]
        offset_x, offset_y = (x - old_center_x, y - old_center_y)
        new_x, new_y = (offset_x + new_center_x, offset_y + new_center_y)
        new_piece.append((new_x, new_y, label))
    return tuple(new_piece)


def rotate_left(state):
    piece, grid = state
    center_x, center_y = piece[0]
    new_piece = [piece[0]]
    for i in range(1, len(piece)):
        x, y, label = piece[i]
        offset_x, offset_y = (x - center_x, y - center_y)
        new_offset_x, new_offset_y = (offset_y, -1 * offset_x)
        new_x, new_y = (new_offset_x + center_x, new_offset_y + center_y)
        new_piece.append((new_x, new_y, label))
    return tuple(new_piece), grid


def hard_drop(state):
    """Move the current piece down until it can't go down anymore, then lock it"""
    pass


def lock(state):
    """If a piece can rest on the brickstack, rest it"""
    piece, grid = state
    pass


def rotate_right(state):
    piece, grid = state
    center_x, center_y = piece[0]
    new_piece = [piece[0]]
    for i in range(1, len(piece)):
        x, y, label = piece[i]
        offset_x, offset_y = (x - center_x, y - center_y)
        new_offset_x, new_offset_y = (-1 * offset_y, offset_x)
        new_x, new_y = (new_offset_x + center_x, new_offset_y + center_y)
        new_piece.append((new_x, new_y, label))
    return tuple(new_piece), grid


def is_legal(state):
    """State is illegal if the piece is oob or intersecting
    Going over the top is not oob
    """
    piece, grid = state
    for i in range(1, len(piece)):
        x, y, label = piece[i]
        if x < 0 or x >= len(grid[0]) or y < 0 or grid[y][x] != " ":
            return False
    return True
