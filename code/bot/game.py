#!/usr/bin/env python3

import random

T_PIECE = ((0, 0), (0, -1, "r"), (-1, 0, "r"), (0, 0, "r"), (1, 0, "r"))

PIECES = [T_PIECE]

class TetrisGame():
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
        pass

    def get_initial_state():
        return send_garbage(generate_state(), "c", 9, 1)

    def is_terminal(state):
        piece, grid = state
        return grid[len(grid)-1][0] != "c"

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
            to_hole -=1
        new_grid.append(garbage_row)
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
