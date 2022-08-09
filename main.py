"""Module for running main logic of program."""
import curses
import os
import random
import time
from pathlib import PurePath, Path

from curses_tools import get_frames
from game_constants import TIC_TIMEOUT, STARS_AMOUNT, STARS_SYMBOLS, BORDER_THICKNESS, START_RANDINT, DIM_DURATION
from engine.async_animations import blink, animate_spaceship, fill_orbit_with_garbage


def draw(canvas: curses.window) -> None:
    """
    This function like event loop, use for register and running tasks.
    :param canvas: place for render all animation.
    """
    from engine.async_animations import coroutines

    canvas.border()
    curses.curs_set(False)
    rows_number, columns_number = canvas.getmaxyx()  # Return a tuple (y, x) of the height and width of the window.
    abs_base_path = Path('frames').absolute()
    all_dirs = os.walk(abs_base_path)
    _, sub_dirs, _ = next(all_dirs)
    frames = []

    for dir in sub_dirs:
        frames.append(get_frames(path=PurePath.joinpath(abs_base_path, dir)))

    spaceship_frames = frames[0]
    garbage_frames = frames[1]
    game_over_frame = frames[2][0]

    for star in range(STARS_AMOUNT):
        row = random.randint(0, rows_number - BORDER_THICKNESS)
        column = random.randint(START_RANDINT, columns_number - BORDER_THICKNESS)
        coroutine = blink(
            canvas=canvas, row=row, column=column, symbol=random.choice(STARS_SYMBOLS),
            offset_tics=random.randint(START_RANDINT, DIM_DURATION),
        )
        coroutines.append(coroutine)

    spaceship_coroutine = animate_spaceship(
        canvas=canvas,
        rows_number=rows_number, columns_number=columns_number, frames=spaceship_frames, game_over=game_over_frame,
    )
    garbage_coroutine = fill_orbit_with_garbage(canvas=canvas, frames=garbage_frames, columns_number=columns_number)
    coroutines.extend([spaceship_coroutine, garbage_coroutine])

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
            if not coroutines:
                break
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
