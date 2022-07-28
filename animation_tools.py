import asyncio
import curses
import random
import time
from itertools import cycle
from pathlib import Path, PurePath

from curses_tools import draw_frame, read_controls, get_frame_size
from game_constants import START_RANDINT, DIM_DURATION, NORMAL_DURATION, BRIGHT_DURATION, BORDER_THICKNESS


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


async def animate_spaceship(canvas, row, column, max_row, max_column):
    dir_path = Path('frames/rocket').absolute()

    for frame in cycle(Path.iterdir(dir_path)):
        with open(PurePath.joinpath(dir_path, frame), 'r') as spaceship_frame:
            file_content = spaceship_frame.read()

        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        frame_rows, frame_columns = get_frame_size(file_content)

        row = min(row + rows_direction, max_row - frame_rows - BORDER_THICKNESS)
        row = max(row, BORDER_THICKNESS)
        column = min(column + columns_direction, max_column - frame_columns - BORDER_THICKNESS)
        column = max(column, BORDER_THICKNESS)

        await animate_spaceship_tool(canvas, row, column, file_content)


async def animate_spaceship_tool(canvas, row, column, file_content):
    draw_frame(canvas, row, column, file_content)
    canvas.refresh()
    await asyncio.sleep(0)
    draw_frame(canvas, row, column, file_content, negative=True)
