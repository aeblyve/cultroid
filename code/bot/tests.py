#!/usr/bin/env python3

import unittest
import game


class TestState(unittest.TestCase):
    def test_repr(self):
        state = game.new_cheese_state(piece=game.T_PIECE)
        print(state)
        state = state.move_anchor(0, 1)
        print(state)


if __name__ == "__main__":
    unittest.main()
