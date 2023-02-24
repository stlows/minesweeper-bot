from tkinter.tix import CELL
import keyboard
import time
from constants import *
import pyautogui
from PIL import Image
from MinesweeperGrid import *

BOARD_WIDTH = CELL_WIDTH * GRID_WIDTH + 2 * OUTSIDE_BORDER
SCREEN_WIDTH = 1920

BOARD_START_X = (SCREEN_WIDTH - BOARD_WIDTH) / 2 + 10 # 471
BOARD_START_Y = 204

def coordToScreen(row, col):
    (x, y) = boardToCoord(row, col)
    return (x + BOARD_START_X, y + BOARD_START_Y, CELL_WIDTH - BORDER, CELL_WIDTH - BORDER)


def boardRegion():
    return (BOARD_START_X, BOARD_START_Y, (CELL_WIDTH) * GRID_WIDTH, (CELL_WIDTH) * GRID_HEIGHT)


def boardToCoord(row, col):
    return (col * CELL_WIDTH + BORDER, row * CELL_WIDTH + BORDER)


def loadBoard():
    board_region = boardRegion()
    gamezone_screenshot = pyautogui.screenshot(region=board_region)
    return MinesweeperGrid(gamezone_screenshot)

def flag(tile):
  row,col,v = tile
  coord = coordToScreen(row, col)
  pyautogui.rightClick(pyautogui.center(coord))

def open(tile):
  row,col,v = tile
  coord = coordToScreen(row, col)
  pyautogui.click(pyautogui.center(coord))


def match(im, row, col):
    (x, y) = boardToCoord(row, col)
    pixel_of_interest_1 = im.getpixel((x + 10, y + 23))
    pixel_of_interest_2 = im.getpixel((x, y))
    pixel_of_interest_3 = im.getpixel((x + 12, y + 13))
    #print(pixel_of_interest_1, pixel_of_interest_2, pixel_of_interest_3)
    if pixel_of_interest_1 == BLACK and pixel_of_interest_2 == RED:
        return -10
    if pixel_of_interest_1 == BLUE:
        return 1
    if pixel_of_interest_1 == GREEN:
        return 2
    if pixel_of_interest_1 == RED:
        return 3
    if pixel_of_interest_3 == VIOLET:
        return 4
    if pixel_of_interest_3 == DARK_RED:
        return 5
    if pixel_of_interest_1 == CYAN:
        return 6
    if pixel_of_interest_1 == GREY and pixel_of_interest_2 == GREY:
        return -1  # opened
    if pixel_of_interest_1 == BLACK:
        return -2  # flag
    if pixel_of_interest_2 == WHITE:
        return 0  # unopened
