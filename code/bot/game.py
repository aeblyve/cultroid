#!/usr/bin/env python3

import random

T_PIECE = ((0, 0), (0, -1, "b"), (-1, 0, "b"), (0, 0, "b"), (1, 0, "b"))
L_PIECE = ((0, 0), (0, 0, "b"), (1, 0, "b"), (0, -1, "b"), (0, -2, "b"))
J_PIECE = ((0, 0), (0, 0, "b"), (-1, 0, "b"), (0, -1, "b"), (0, -2, "b"))
O_PIECE = ((0, 0), (0, 0, "b"), (1, 0, "b"), (0, -1, "b"), (1, -1, "b"))
S_PIECE = ((0, 0), (0, 0, "b"), (-1, 0, "b"), (0, -1, "b"), (1, -1, "b"))
Z_PIECE = ((0, 0), (0, 0, "b"), (-1, 0, "b"), (0, -1, "b"), (1, -1, "b"))
I_PIECE = ((0, 0), (0, 0, "b"), (0, -1, "b"), (0, -2, "b"), (0, -3, "b"))

PIECES = [T_PIECE, L_PIECE, J_PIECE, O_PIECE, S_PIECE, Z_PIECE, I_PIECE]
# TODO set up gamestate/successor


class TetrisGame:
    """A problem statement for a tetris-like game"""

    pass


class CheeseGame(TetrisGame):
    def get_successors(state):
        """
        You can:
        + Move down
        + Move right
        + Move left
        + Rotate
        Each is "one state".
        """
        piece, grid = state
        center_x, center_y = piece[0]
        # compute all states: only return valid ones
        go_down_state = (recenter_piece(piece, (center_x, center_y - 1)), grid)
        go_right_state = (recenter_piece(piece, (center_x + 1, center_y)), grid)
        go_left_state = (recenter_piece(piece, (center_x - 1, center_y)), grid)
        rotate_left_state = rotate_left(state)
        rotate_right_state = rotate_right(state)
        # TODO: "lock in state"
        # TODO: "hard drop" state
        states = [
            go_down_state,
            go_right_state,
            go_left_state,
            rotate_left_state,
            rotate_right_state,
        ]
        return list(filter(is_legal), states)

    def get_initial_state(self):
        return send_garbage(generate_state(), "c", 9, 1)

    def is_terminal(state):
        piece, grid = state
        return grid[len(grid) - 1][0] != "c"


"Note: It might not be a bad idea to have the state/grid as an object" "We would just have to have it be immutable after initalization and we could use it like tuples " "(and have all functions which change it just retrun the succesor object without mutation)" "It may be more effor than it's worth but that way if we need to make any changes it won't have" "to be so hard coded"


def state2string(state):
    piece, grid = state
    rep = []
    st = ""
    for row in grid:
        rep.append(row)
    for i in range(1, len(piece)):
        x, y, label = piece[i]
        if x in range(len(grid[0])) and y in range(len(grid)):
            rep[y] = rep[y][:x] + label + rep[y][x:-1]
    for row in rep:
        st += "|" + row + "|\n"
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
