# Bot that can resolve minsweeper on https://minesweeperonline.com/#200

1. Set game mode to Expert
1. Make sure it is full screen and display zoom 200%
1. Validate the board region is good for your display using uni tests. `python tests.py`
1. You can adjust it using the code `pyautogui.screenshot("img/temp.png" region=ui.boardRegion())` and validate that you see the whole board.
1. Start new game but don't click on any square
1. Run `python main.py` on another screen.
1. Enjoy
