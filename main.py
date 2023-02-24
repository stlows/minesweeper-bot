from logging import PercentStyle
import pyautogui
import time
from PIL import Image
import math
import numpy as np
from constants import *
import ui

def game_loop(depth=1):
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
    return game_loop(depth+1)
  for open in openable:
    ui.open(open)
  for flag in flaggable:
    ui.flag(flag)
  return game_loop(depth+1)

def random():
  board = ui.loadBoard()
  random, perc_of_bomb = board.random_pick()
  #print("Opening: ", random, " Chance of bomb: ", perc_of_bomb)
  ui.open(random)
  time.sleep(0.01)
  board = pyautogui.screenshot(region=ui.boardRegion())
  match = ui.match(board, random[0], random[1])
  #print("It was a:", match)
  if match == -10:
    return False
  return True

pyautogui.PAUSE = 0.01

def start_game():
  first = (GRID_HEIGHT/2,GRID_WIDTH/2,0)
  ui.open(first)
  board = pyautogui.screenshot(region=ui.boardRegion())
  match = ui.match(board, first[0], first[1])
  if match != -10:
    game_loop()
  

start_game()
# python -m cProfile -s time main.py > log.txt

# board = pyautogui.screenshot("img/temp.png",region=ui.boardRegion())
# match = ui.match(board, 2, 29)
# print(match)

