import curses
import random
import time

from animation_tools import fire, blink, animate_spaceship
from game_constants import (TIC_TIMEOUT, STARS_AMOUNT, STARS_SYMBOLS, BORDER_THICKNESS, START_RANDINT, )


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    max_row, max_column = canvas.getmaxyx()
    coroutines = []

    for star in range(STARS_AMOUNT):
        row = random.randint(0, max_row - BORDER_THICKNESS)
        column = random.randint(START_RANDINT, max_column - BORDER_THICKNESS)
        coroutine = blink(canvas=canvas, row=row, column=column, symbol=random.choice(STARS_SYMBOLS))
        coroutines.append(coroutine)

    fire_coroutine = fire(
        canvas=canvas, start_row=max_row - BORDER_THICKNESS,
        start_column=max_column - BORDER_THICKNESS, rows_speed=-1,
    )
    spaceship_coroutine = animate_spaceship(canvas, row=5, column=50)
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
    while True:
        curses.wrapper(draw)
