"""Module for running main logic of program."""
import curses
import random
import time
from collections import defaultdict
from pathlib import PurePath, Path

from curses_tools import get_frames
from engine.async_animations import blink, animate_spaceship, fill_orbit_with_garbage, count_year, coroutines, show_year
from game_constants import TIC_TIMEOUT, STARS_AMOUNT, STARS_SYMBOLS, BORDER_THICKNESS, START_RANDINT, DIM_DURATION


def draw(canvas: curses.window) -> None:
    """
    This function like event loop, use for register and running tasks.
    :param canvas: place for render all animation.
    """
    canvas.border()
    sub_window = canvas.derwin(0, 0)
    curses.curs_set(False)
    rows_number, columns_number = canvas.getmaxyx()  # Return a tuple (y, x) of the height and width of the window.
    abs_base_path = Path('frames').absolute()

    frame_dirs = ['rocket', 'garbage', 'screensavers']
    frames = defaultdict(list)

    for directory in frame_dirs:
        frames[directory] = get_frames(path=PurePath.joinpath(abs_base_path, directory))

    for star in range(STARS_AMOUNT):
        row = random.randint(0, rows_number - BORDER_THICKNESS)
        column = random.randint(START_RANDINT, columns_number - BORDER_THICKNESS)
        coroutine = blink(
            canvas=canvas, row=row, column=column, symbol=random.choice(STARS_SYMBOLS),
            offset_tics=random.randint(START_RANDINT, DIM_DURATION),
        )
        coroutines.append(coroutine)

    year_count_cor = count_year()
    show_year_cor = show_year(sub_window)
    spaceship_coroutine = animate_spaceship(
        canvas=canvas,
        rows_number=rows_number, columns_number=columns_number, frames=frames['rocket'],
        game_over=frames['screensavers'][0],
    )
    garbage_coroutine = fill_orbit_with_garbage(canvas=canvas, frames=frames['garbage'], columns_number=columns_number)
    coroutines.extend([year_count_cor, show_year_cor, spaceship_coroutine, garbage_coroutine])

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
