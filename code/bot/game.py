#!/usr/bin/env python3

import random, copy
from enum import Enum

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


class CheeseActions(Enum):
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    RLEFT = 4
    RRIGHT = 5
    LOCK = 6
    HARD = 7


class CheeseGame:
    """Clear all the cheese to win."""

    def __init__(self):
        self.randomizer = SimpleRandomizer(PIECES)

    def get_start_state(self):
        return new_cheese_state(x_dimension=10, y_dimension=20)

    def get_successors(self, state):

        go_down_succ = state.move_anchor(0, 1)
        go_left_succ = state.move_anchor(-1, 0)
        go_right_succ = state.move_anchor(1, 0)
        rotate_left_succ = state.rotate_left()
        rotate_right_succ = state.rotate_right()
        lock_succ = state.lock_piece(self.randomizer)
        hard_succ = state.hard_drop(self.randomizer)
        # each action costs 1
        successors = [
            (go_down_succ, CheeseActions.DOWN, 1),
            (go_left_succ, CheeseActions.LEFT, 1),
            (go_right_succ, CheeseActions.RIGHT, 1),
            (rotate_left_succ, CheeseActions.RLEFT, 1),
            (rotate_right_succ, CheeseActions.RRIGHT, 1),
            (lock_succ, CheeseActions.LOCK, 1),
            (hard_succ, CheeseActions.HARD, 1),
        ]

        return filter(lambda x: x[0].is_legal(), successors)

    # def is_terminal(self, state):
    #     """Illegal states and cleared cheese is terminal
    #     If terminal, return the utility, else 0
    #     """
    #     if not state.is_legal():
    #         return -100
    #     elif state.is_clear():
    #         return 100
    #     else:
    #         return 0

    def is_goal(self, state):
        return state.is_clear()


class Randomizer:
    pass


def row_is_full(row):
    for block in row:
        if block == BLANK_LABEL:
            return False
    return True


def clear_rows(grid):
    """Clear full rows."""
    y_dimension = len(grid)
    x_dimension = len(grid[0])
    blank_row = tuple([BLANK_LABEL] * x_dimension)
    filtered = list(filter(lambda x: not row_is_full(x), grid))
    for _ in range(y_dimension - len(filtered)):
        filtered.insert(0, blank_row)
    return tuple(filtered)


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

    def is_clear(self):
        """If the last row is clear, the whole stage is"""
        return self.grid[len(self.grid) - 1][0] != CHEESE_LABEL

    def is_legal(self):
        """Illegal if oob or intersecting"""
        for x, y, label in self.piece:
            if (
                x < 0
                or x >= len(self.grid[0])
                or y < 0
                or self.grid[y][x] != BLANK_LABEL
            ):
                return False
        return True

    def can_lock(self):
        for x, y, label in self.piece:
            if y == len(self.grid) - 1 or self.grid[y + 1][x] != BLANK_LABEL:
                return True
        return False

    def lock_piece(self, randomizer):
        """Fix the current piece to the board if possible, and get a new one"""
        # TODO suboptimal
        can_lock = self.can_lock()
        if can_lock and self.is_legal():
            new_grid = []
            for row in self.grid:
                new_grid.append(list(row))
            for x, y, label in self.piece:
                new_grid[y][x] = label
            for i in range(len(new_grid)):
                new_grid[i] = tuple(new_grid[i])
            new_grid = tuple(new_grid)
            new_grid = clear_rows(new_grid)
            new_piece = randomizer.choice()
            mapped_piece = shift_piece(new_piece, self.spawn[0], self.spawn[1])

            return CheeseState(self.spawn, self.spawn, mapped_piece, new_grid)
        else:
            return CheeseState(self.spawn, self.anchor, self.piece, self.grid)

    def hard_drop(self, randomizer):
        y_delta = float("inf")

        for x, y, label in self.piece:
            for y_i in range(y, len(self.grid)):
                if self.grid[y_i][x] != BLANK_LABEL and not y < 0:
                    y_delta = min(y_delta, y_i - y)
                    break

        new_state = self.move_anchor(0, y_delta - 1)
        return new_state.lock_piece(randomizer)

    def __repr__(self):
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

    def rotate_left(self):
        new_piece = []
        anchor_x, anchor_y = self.anchor
        for x, y, label in self.piece:
            offset_x, offset_y = (x - anchor_x, y - anchor_y)
            new_offset_x, new_offset_y = (offset_y, -1 * offset_x)
            new_x, new_y = (new_offset_x + anchor_x, new_offset_y + anchor_y)
            new_piece.append((new_x, new_y, label))
        new_piece = tuple(new_piece)
        return CheeseState(self.spawn, self.anchor, new_piece, self.grid)

    def rotate_right(self):
        new_piece = []
        anchor_x, anchor_y = self.anchor
        for x, y, label in self.piece:
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
