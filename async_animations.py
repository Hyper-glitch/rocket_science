"""Module that helps animate frames."""
import asyncio
import curses
from itertools import cycle

from curses_tools import draw_frame, read_controls, get_frame_size
from game_constants import DIM_DURATION, NORMAL_DURATION, BRIGHT_DURATION, BORDER_THICKNESS
from physics import update_speed


async def blink(canvas: curses.window, row: int, column: int, symbol: str, offset_tics: int) -> None:
    """
    Animate stars blink asynchronously.
    :param canvas: place for rendering animation.
    :param row: Y canvas coordinate.
    :param column: X canvas coordinate.
    :param symbol: symbol for rendering on canvas.
    :param offset_tics: parameter that control offset tics.
    :return: None
    """
    canvas.addstr(row, column, symbol, curses.A_DIM)
    await sleep(tics=offset_tics)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(tics=DIM_DURATION)

        canvas.addstr(row, column, symbol)
        await sleep(tics=NORMAL_DURATION)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(tics=BRIGHT_DURATION)

        canvas.addstr(row, column, symbol)
        await sleep(tics=NORMAL_DURATION)


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


async def animate_spaceship(
        canvas: curses.window, row: int, column: int,
        rows_number: int, columns_number: int, frames: list,
) -> None:
    """
    Animate spaceship frames.
    :param canvas: place for rendering animation.
    :param row: Y-canvas coordinate.
    :param column: X-canvas coordinate.
    :param rows_number: height of the window.
    :param columns_number: width of the window.
    :param frames: content, that reads from txt file.
    :return: None
    """
    for frame in cycle(frames):

        for _ in range(2):
            row_speed = column_speed = 0
            rows_direction, columns_direction, space_pressed = read_controls(canvas)
            frame_rows, frame_columns = get_frame_size(frame)

            row = min(row + rows_direction, rows_number - frame_rows - BORDER_THICKNESS)
            row = max(row, BORDER_THICKNESS)
            column = min(column + columns_direction, columns_number - frame_columns - BORDER_THICKNESS)
            column = max(column, BORDER_THICKNESS)

            row_speed, column_speed = update_speed(
                row_speed=row_speed, column_speed=column_speed, rows_direction=rows_direction,
                columns_direction=columns_direction,
            )
            draw_frame(canvas, row + row_speed, column + column_speed, frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row + row_speed, column + column_speed, frame, negative=True)


async def fly_garbage(canvas, column, frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""

    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)
        row += speed


async def sleep(tics):
    """
    Custom sleep for make ping in code.
    :param tics: amount of iterations.
    """
    for _ in range(tics):
        await asyncio.sleep(0)
