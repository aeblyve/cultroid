#!/usr/bin/env python3

import unittest
import game

class TestState(unittest.TestCase):


    def test_repr(self):
        state = game.generate_state()
        print("Behold a tetris state:")
        print(game.state2string(state))
        state = game.rotate_piece(state)
        print("Behold a rotation:")
        print(game.state2string(state))
        state = game.send_garbage(state, "c", 9, 3)
        print("Behold some trash:")
        print(game.state2string(state))






if __name__ == "__main__":
    unittest.main()
