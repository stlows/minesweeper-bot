from operator import ne
from tkinter import N
import numpy as np
from constants import *
import ui


class MinesweeperGrid:

    def check_impasse(self, board):
      h, w = board.shape
      for row in range(0, h):
          for col in range(0, w):
              if(board[row, col]) > 0:
                  neighbours = self.get_neighbours(board, row, col)
                  unopened_around = [x for x in neighbours if x[2] == 0]
                  flags_around = [x for x in neighbours if x[2] == -2]
                  remaining = board[row, col] - len(flags_around)
                  if remaining > len(unopened_around) or len(flags_around) > board[row, col]:
                    return True
      return False
      
    def level_2_find(self):
      h, w = self.tiles.shape
      for row in range(0, h):
          for col in range(0, w):
              if(self.tiles[row, col]) > 0:
                  neighbours = self.get_neighbours(self.tiles, row, col)
                  unopened_around = [x for x in neighbours if x[2] == 0]
                  flags_around = [x for x in neighbours if x[2] == -2]
                  remaining_flags = self.tiles[row, col] - len(flags_around)
                  remaining_to_open = len(unopened_around) - self.tiles[row, col]
                  if remaining_flags == 1: # S'il reste juste une bombe parmi les non-ouvert on simule les bombes de chacun
                    for unopened in unopened_around:
                      board_copy = np.copy(self.tiles)
                      board_copy[unopened[0], unopened[1]] = -2
                      (openable, flaggable) = self.level_1_find(board_copy)
                      for open in openable:
                        board_copy[open[0], open[1]] = -1
                      for flag in flaggable:
                        board_copy[flag[0], flag[1]] = -2
                      if self.check_impasse(board_copy):
                        #print("Found impasse based on", row, col)
                        return unopened, "open"
                  if remaining_to_open == 1: # S'il en reste juste un à ouvrir parmi les non-ouvert on simule les ouvertures de chacun
                    for unopened in unopened_around:
                      board_copy = np.copy(self.tiles)
                      board_copy[unopened[0], unopened[1]] = -1
                      (openable, flaggable) = self.level_1_find(board_copy)
                      for open in openable:
                        board_copy[open[0], open[1]] = -1
                      for flag in flaggable:
                        board_copy[flag[0], flag[1]] = -2
                      if self.check_impasse(board_copy):
                        #print("Found impasse based on", row, col)
                        return unopened, "flag"
      return None

    def random_pick(self):
      percentage = 1
      openable = []
      h, w = self.tiles.shape
      for row in range(0, h):
          for col in range(0, w):
              if(self.tiles[row, col]) > 0:
                  neighbours = self.get_neighbours(self.tiles, row, col)
                  unopened_around = [x for x in neighbours if x[2] == 0]
                  flags_around = [x for x in neighbours if x[2] == -2]
                  remaining = self.tiles[row, col] - len(flags_around)
                  new_percentage = remaining / len(unopened_around)
                  if new_percentage < percentage:
                    percentage = new_percentage
                    openable = unopened_around[0]
      return (openable, percentage)

    def level_1_find(self, tiles):
        openable = []
        flaggable = []
        h, w = self.tiles.shape
        for row in range(0, h):
          for col in range(0, w):
            value = self.tiles[row, col]
            if(value) > 0:
              neighbours = self.get_neighbours(tiles, row, col)
              flags_around = [x for x in neighbours if x[2] == -2]
              unopened_around = [x for x in neighbours if x[2] == 0]
              if(len(flags_around) == value and len(unopened_around) > 0):
                openable.extend([x for x in unopened_around if x not in openable])
              if(len(flags_around) + len(unopened_around) == value and len(unopened_around) > 0):
                flaggable.extend([x for x in unopened_around if x not in flaggable])
        return openable,flaggable

    def get_neighbours_values_list(self, tiles, row, col):
        return np.array(self.get_neighbours(tiles, row, col))[:, 2].tolist()

    def get_neighbours(self, tiles, row, col):
        neighbours = []
        h, w = tiles.shape
        if row > 0 and col > 0:
            neighbours.append((row-1, col-1, tiles[row-1, col-1]))
        if row > 0:
            neighbours.append((row-1, col, tiles[row-1, col]))
        if row > 0 and col < w - 1:
            neighbours.append((row-1, col+1, tiles[row-1, col + 1]))
        if col > 0:
            neighbours.append((row, col-1, tiles[row, col-1]))
        if col < w - 1:
            neighbours.append((row, col+1, tiles[row, col + 1]))
        if row < h - 1 and col > 0:
            neighbours.append((row+1, col-1, tiles[row+1, col - 1]))
        if row < (h - 1):
            neighbours.append((row+1, col, tiles[row+1, col]))
        if row < h - 1 and col < w - 1:
            neighbours.append((row+1, col+1, tiles[row+1, col + 1]))
        return neighbours

    def toTilesArray(self, tiles):
      return [[(row, col, tiles[row,col]) for col in range(0, GRID_WIDTH)] for row in range(0, GRID_HEIGHT)]

    def __init__(self, im):
        tiles = np.zeros((GRID_HEIGHT, GRID_WIDTH))
        for y in range(0, GRID_HEIGHT):
            for x in range(0, GRID_WIDTH):
                match = ui.match(im, y, x)
                tiles[y][x] = match
        self.tiles = tiles
        self.tilesArray = self.toTilesArray(tiles)