import unittest
import numpy as np
from MinesweeperGrid import *
from PIL import Image
import pyautogui


class TetrisTests(unittest.TestCase):

    def test_recognition(self):
        gamezone_screenshot = Image.open("img/game_test_1.png")
        tiles = MinesweeperGrid(gamezone_screenshot).tiles
        self.assertEqual(-1, tiles[0][0])  # opened
        self.assertEqual(0, tiles[0][3])  # unopened
        self.assertEqual(-2, tiles[0][2])  # flag
        self.assertEqual(1, tiles[0][1])  # 1
        self.assertEqual(2, tiles[1][1])  # 2
        self.assertEqual(3, tiles[3][3])  # 3
        self.assertEqual(4, tiles[1][2])  # 4

    def test_neighbors(self):
        gamezone_screenshot = Image.open("img/game_test_1.png")
        board = MinesweeperGrid(gamezone_screenshot)
        self.assertEqual([1, -1, 2], board.get_neighbours_values_list(board.tiles, 0, 0))
        self.assertEqual([-1, -2, -1, 2, 4], board.get_neighbours_values_list(board.tiles, 0, 1))
        self.assertEqual([0, 0, 0], board.get_neighbours_values_list(board.tiles, 0, 29))
        self.assertEqual([2, 3, 2, 1, 2], board.get_neighbours_values_list(board.tiles, 14, 0))
        self.assertEqual([2, 3, 2, -2, -2, 1, 2, 2], board.get_neighbours_values_list(board.tiles, 14, 1))
        self.assertEqual([-2, 2, 2], board.get_neighbours_values_list(board.tiles, 15, 0))
        self.assertEqual([-2, 2, -2, 1, 2], board.get_neighbours_values_list(board.tiles, 15, 1))
        self.assertEqual([0, 0, 0], board.get_neighbours_values_list(board.tiles, 15, 29))

if __name__ == "__main__":
    unittest.main()
