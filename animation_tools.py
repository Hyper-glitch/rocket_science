import asyncio
import curses
import random
import time
from itertools import cycle
from pathlib import Path, PurePath

from curses_tools import draw_frame
from game_constants import START_RANDINT, DIM_DURATION, NORMAL_DURATION, BRIGHT_DURATION


async def blink(canvas, row, column, symbol):
    canvas.addstr(row, column, symbol, curses.A_DIM)
    for _ in range(random.randint(START_RANDINT, DIM_DURATION)):
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(DIM_DURATION):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(NORMAL_DURATION):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(BRIGHT_DURATION):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(NORMAL_DURATION):
            await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display frames of gun shot, direction and speed can be specified."""
    row, column = start_row, start_column
    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def animate_spaceship(canvas, row, column):
    dir_path = Path('frames/rocket').absolute()

    for frame in cycle(Path.iterdir(dir_path)):
        with open(PurePath.joinpath(dir_path, frame), 'r') as first_frame:
            first_file_content = first_frame.read()

        animate_spaceship_tool(canvas, row, column, first_file_content)
        draw_frame(canvas, row, column, first_file_content, negative=True)


def animate_spaceship_tool(canvas, row, column, file_content):
    draw_frame(canvas, row, column, file_content)
    canvas.refresh()
    time.sleep(1)
