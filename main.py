"""Module for running main logic of program."""
import curses
import random
import time

from animation_tools import fire, blink, animate_spaceship, get_frames_content
from game_constants import TIC_TIMEOUT, STARS_AMOUNT, STARS_SYMBOLS, BORDER_THICKNESS, START_RANDINT, DIM_DURATION


def draw(canvas) -> None:
    """
    This function like event loop, use for register and running tasks.
    :param canvas: place for render all animation.
    """
    canvas.border()
    curses.curs_set(False)
    rows_number, columns_number = canvas.getmaxyx()  # Return a tuple (y, x) of the height and width of the window.
    coroutines = []

    for star in range(STARS_AMOUNT):
        row = random.randint(0, rows_number - BORDER_THICKNESS)
        column = random.randint(START_RANDINT, columns_number - BORDER_THICKNESS)
        coroutine = blink(
            canvas=canvas, row=row, column=column, symbol=random.choice(STARS_SYMBOLS),
            offset_tics=random.randint(START_RANDINT, DIM_DURATION),
        )
        coroutines.append(coroutine)

    frames_content = get_frames_content()

    fire_coroutine = fire(
        canvas=canvas, start_row=rows_number - BORDER_THICKNESS,
        start_column=columns_number - BORDER_THICKNESS, rows_speed=-1,
    )
    spaceship_coroutine = animate_spaceship(
        canvas, row=rows_number // 2, column=columns_number // 2,
        rows_number=rows_number, columns_number=columns_number, frames_content=frames_content,
    )

    coroutines.extend([fire_coroutine, spaceship_coroutine])

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
