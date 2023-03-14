from logging import PercentStyle
import pyautogui
import time
from PIL import Image
import math
import numpy as np
from constants import *
import ui

mines_left = MINES[DIFFICULTY]

def game_loop(depth=1):
  global mines_left
  if depth > 120:
    print("120 calls, we stop")
    return False
  board = ui.loadBoard()
  if board is None:
    return False
  (openable, flaggable) = board.level_1_find(board.tiles)
  if(len(flaggable) == 0 and len(openable) == 0):
    #print("Level 2 finding:")
    find = board.level_2_find()
    if find is None:
      if random():
        return game_loop(depth+1)
      else:
        return False
    #print(find)
    if(find[1] == "open"):
      ui.open(find[0])
    if(find[1] == "flag"):
      ui.flag(find[0])
      mines_left = mines_left - 1
  else:
    for open in openable:
      ui.open(open)
    for flag in flaggable:
      ui.flag(flag)
      mines_left = mines_left - 1
  if mines_left == 0:
    print("No more mines to find, opening all unopened tiles.")
    board = ui.loadBoard()
    for open in board.all_unopened(board.tiles):
      ui.open(open)
    return False
  return game_loop(depth+1)

def random():
  board = ui.loadBoard()
  random, perc_of_bomb = board.random_pick()
  #print("Opening: ", random, " Chance of bomb: ", perc_of_bomb)
  ui.open(random)
  time.sleep(0.01)
  board = pyautogui.screenshot("img/random.png", region=ui.boardRegion())
  match = ui.match(board, random[0], random[1], withlog=False)
  print("Random Time ! It was a:", match, random)
  if match == -10:
    return False
  return True

pyautogui.PAUSE = 0.01

def start_game(nofirstclick=False):

  dead_face = pyautogui.locateOnScreen("img/dead_face.png")
  if dead_face is not None:
    pyautogui.click(pyautogui.center(dead_face))
  if nofirstclick:
    return game_loop()
  first = (GRID_HEIGHT[DIFFICULTY]/2,GRID_WIDTH[DIFFICULTY]/2,0)
  ui.open(first)
  time.sleep(0.05)
  board = pyautogui.screenshot(region=ui.boardRegion())
  time.sleep(0.05)
  match = ui.match(board, first[0], first[1])
  if match != -10:
    game_loop()

start_game()

# python -m cProfile -s time main.py > log.txt

#board = pyautogui.screenshot("img/temp_" + str(DIFFICULTY) + ".png",region=ui.boardRegion())
#match = ui.match(board, 8, 28, withlog=True)
#print(match)

# dead_face = pyautogui.locateOnScreen("img/dead_face.png")
# if dead_face is not None:
#   pyautogui.click(pyautogui.center(dead_face))

