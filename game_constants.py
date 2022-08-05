""" Module with constants using in space game. """
from enum import Enum

TIC_TIMEOUT = 0.1
DIM_DURATION = 20
NORMAL_DURATION = 3
BRIGHT_DURATION = 5
STARS_SYMBOLS = '+*.:'
STARS_AMOUNT = 500
BORDER_THICKNESS = 2
START_RANDINT = 0
FRAME_RATE = 15


class KeyCode(Enum):
    """Class for keeping key codes digits."""
    SPACE = 32
    LEFT = 260
    RIGHT = 261
    UP = 259
    DOWN = 258
