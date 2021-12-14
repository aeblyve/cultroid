import random

"Abstraction for Piece, Stores necessary data and some basic functions"
class Piece:
    def __init__(self, center, positions, label):
        self.center = center
        self.positions = positions
        self.label = label

    def rotate_left(self):
        new_piece = []
        anchor_x, anchor_y = self.center
        for x, y in self.positions:
            offset_x, offset_y = (x - anchor_x, y - anchor_y)
            new_offset_x, new_offset_y = (offset_y, -1 * offset_x)
            new_x, new_y = (new_offset_x + anchor_x, new_offset_y + anchor_y)
            new_piece.append((new_x, new_y))
        new_piece = tuple(new_piece)
        return Piece(self.center, new_piece, self.label)

    def change_center(self, shiftamount):
        new_piece = []
        change_x, change_y = shiftamount
        for x, y in self.positions:
            new_piece.append((x + change_x, y + change_y))
        new_piece = tuple(new_piece)
        return Piece((self.center[0] + change_x, self.center[1] + change_y), new_piece, self.label)

    def bound_ranges(self):
        max_x = None
        max_y = None
        min_x = None
        min_y = None
        for x, y in self.positions:
            if max_x is None or x > max_x:
                max_x = x
            if max_y is None or y > max_y:
                max_y = y
            if min_x is None or x < min_x:
                min_x = x
            if min_y is None or y < min_y:
                min_y = y
        return (min_x, max_x), (min_y, max_y)

"Class fot build Tetris Grids, supports clogging with random trash"
class TetrisGridBuilder:
    def __init__(self):
        self.grid = [[]]
        self.blank = ""

    def set_blank(self, blank):
        self.blank = blank
        return self

    def set_grid(self, grid):
        self.grid = grid
        return self

    def set_blank_grid(self, width, height, blank):
        self.set_blank(blank)
        row = [blank for i in range(width)]
        grid = [row.copy() for i in range(height)]
        self.set_grid(grid)
        return self

    def new_cheese_state(self,
            x_dimension=10, y_dimension=20, hole_count=1, cheese_count=9, cheese_char="c"):
        self.set_blank_grid(x_dimension, y_dimension, "_")

        for g in range(y_dimension - cheese_count, y_dimension):
            to_hole = hole_count
            cheese_row = [cheese_char] * x_dimension

            while to_hole != 0:
                hole_index = random.choice(range(x_dimension))
                cheese_row[hole_index] = self.blank
                to_hole -= 1
            self.grid[g] = cheese_row
        return self

    def build(self):
        return TetrisGrid(tuple([tuple(row) for row in self.grid]), self.blank)

"Class for Grid"
class Grid:
    def __init__(self, grid, blank):
        self.grid = grid
        self.blank = blank

    def __hash__(self):
        return hash((self.grid, self.blank))

    def __eq__(self, other):
        if isinstance(other, Grid):
            return (other.blank == self.blank) and (other.grid == self.grid)

    def __repr__(self):
        out = ""
        for i in range(len(self.grid)):
            for col in self.grid[i]:
                out += str(col)
            out += " " + str(i) + " \n"
        return out

def row_is_full(row, blank):
    for block in row:
        if block == blank:
            return False
    return True


def clear_rows(grid, blank):
    """Clear full rows."""
    y_dimension = len(grid)
    x_dimension = len(grid[0])
    blank_row = tuple([blank] * x_dimension)
    filtered = list(filter(lambda x: not row_is_full(x, blank), grid))
    for _ in range(y_dimension - len(filtered)):
        filtered.insert(0, blank_row)
    return tuple(filtered)

"Represents the Tetris Grid"
class TetrisGrid(Grid):
   #to drop from sky, merely place piece in the clouds

    def hard_drop(self, piece):
        y_delta = float("inf")

        for x, y in piece.positions:
             for y_i in range(y, len(self.grid)):
                if y_i >= 0 and self.grid[y_i][x] != self.blank:
                    y_delta = min(y_delta, y_i - y)
                    break
             y_delta = min(y_delta, len(self.grid) - y)

        new_piece = piece.change_center((0, y_delta - 1))
        return self.lock_piece(new_piece)

    def lock_piece(self, piece):
        newgrid = [[col for col in row] for row in self.grid]
        for x, y in piece.positions:
            if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
                newgrid[y][x] = piece.label
            else:
                return False
        newgrid = clear_rows(newgrid, self.blank)
        return TetrisGrid(tuple([tuple(row) for row in newgrid]), self.blank)

    #See if a given thing is contained in the grid
    def contains(self, symbol):
        for row in self.grid:
            for col in row:
                if col == symbol:
                    return True
        return False

T_PIECE = Piece((0, 0), ((0, -1), (-1, 0), (0, 0), (1, 0)), "b")
L_PIECE = Piece((0, 0), ((0, 0), (1, 0), (0, -1), (0, -2)), "b")
J_PIECE = Piece((0, 0), ((0, 0), (-1, 0), (0, -1), (0, -2)), "b")
O_PIECE = Piece((0, 0), ((0, 0), (1, 0), (0, -1), (1, -1)), "b")
S_PIECE = Piece((0, 0), ((0, 0), (-1, 0), (0, -1), (1, -1)), "b")
Z_PIECE = Piece((0, 0), ((0, 0), (-1, 0), (0, -1), (1, -1)), "b")
I_PIECE = Piece((0, -1), ((0, 0), (0, -1), (0, -2), (0, -3)), "b")

PIECES = [T_PIECE, L_PIECE, J_PIECE, O_PIECE, S_PIECE, Z_PIECE, I_PIECE]

class CheeseGameLocked:
    """Clear all the cheese to win."""

    def __init__(self, x_dimension=10, y_dimension=20, hole_count=1, cheese_count=9, pieces=PIECES):
        self.x_dimension = x_dimension
        self.y_dimension = y_dimension
        self.hole_count = hole_count
        self.cheese_count = cheese_count
        self.pieces = pieces
        self.reward = lambda before, after: 0

    def get_start_state(self):
        return TetrisGridBuilder().new_cheese_state(self.x_dimension, self.y_dimension,
                                              self.hole_count, self.cheese_count, "c").build()

    def set_reward(self, reward):
        self.reward = reward

    def get_successors(self, state, given=None):
        if given is None:
            piece = random.choice(self.pieces)
        else:
            piece = given
        successors = []
        explored = {False}
        for i in range(4):
            xrange, yrange = piece.bound_ranges()
            piece = piece.change_center((0 - xrange[0], 0 - yrange[1]))
            for offset in range(len(state.grid[0]) - xrange[1] + xrange[0]):
                newstate = state.hard_drop(piece.change_center((offset, 0)))
                if newstate not in explored:
                    successors.append((newstate, (i, offset), self.reward(state, newstate)))
            piece = piece.rotate_left()

        return successors

    def is_goal(self, state):
        return not state.contains("c")