import asyncio
import curses
import random
import time

from game_constants import (
    TIC_TIMEOUT, DIM_DURATION, NORMAL_DURATION, BRIGHT_DURATION, STARS_AMOUNT, STARS_SYMBOLS,
    BORDER_THICKNESS,
)


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    max_row, max_column = canvas.getmaxyx()
    coroutines = []

    for star in range(STARS_AMOUNT):
        row = random.randint(0, max_row - BORDER_THICKNESS)
        column = random.randint(0, max_column - BORDER_THICKNESS)
        coroutine = blink(canvas=canvas, row=row, column=column, symbol=random.choice(STARS_SYMBOLS))
        coroutines.append(coroutine)

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


async def blink(canvas, row, column, symbol):
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


if __name__ == '__main__':
    curses.update_lines_cols()
    while True:
        curses.wrapper(draw)
