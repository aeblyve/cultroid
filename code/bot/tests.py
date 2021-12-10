#!/usr/bin/env python3

import unittest, game, search
from game import BLANK_LABEL


class TestSearch(unittest.TestCase):
    def test_astar(self):
        cheese_game = game.CheeseGame()
        path = search.Astar_search(cheese_game, search.cheese_left_heuristic)
        print(path)

    # def test_tdfs(self):
    #     cheese_game = game.CheeseGame()
    #     path = search.tree_depth_first_search(cheese_game)
    #     print(path)


#     def test_bfs(self):
#     donut run this
#         cheese_game = game.CheeseGame()
#         path = search.breadth_first_search(cheese_game)
#         # and now we wait...
#         print(path)


class TestState(unittest.TestCase):
    def test_repr(self):
        state = game.new_cheese_state(piece=game.T_PIECE)
        print(state)
        state = state.move_anchor(0, 1)
        print(state)
        state = state.rotate_left()
        print(state)
        state = state.rotate_right()
        print(state)

    def test_lock(self):

        simple_grid = (
            (BLANK_LABEL, BLANK_LABEL),
            (BLANK_LABEL, BLANK_LABEL),
            (BLANK_LABEL, "b"),
            (BLANK_LABEL, "b"),
            ("b", BLANK_LABEL),
        )

        simple_piece = (
            (0, 0, "b"),
            (0, -1, "b"),
        )

        new_piece = (
            # it's reD!
            (0, 0, "r"),
            (0, -1, "r"),
        )

        simple_randomizer = game.SimpleRandomizer([new_piece])

        state = game.CheeseState((0, 0), (0, 0), simple_piece, simple_grid)
        assert not state.can_lock()
        state = state.move_anchor(0, 3)
        assert state.can_lock()
        state = state.lock_piece(simple_randomizer)
        print(state)

    def test_drop(self):
        simple_grid = (
            (BLANK_LABEL, BLANK_LABEL),
            (BLANK_LABEL, BLANK_LABEL),
            (BLANK_LABEL, "b"),
            (BLANK_LABEL, "b"),
            ("b", BLANK_LABEL),
        )

        simple_piece = (
            (0, 0, "b"),
            (0, -1, "b"),
        )

        new_piece = (
            # it's reD!
            (0, 0, "r"),
            (0, -1, "r"),
        )

        simple_randomizer = game.SimpleRandomizer([new_piece])

        state = game.CheeseState((0, 0), (0, 0), simple_piece, simple_grid)

        state = state.hard_drop(simple_randomizer)
        print(state)


if __name__ == "__main__":
    unittest.main()
