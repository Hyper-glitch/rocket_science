import asyncio
import curses
import time


TIC_TIMEOUT = 0.1


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    row, column = (5, 20)
    coroutines = []
    stars_amount = 5

    for star in range(stars_amount):
        coroutine = blink(canvas=canvas, row=row, column=column)
        coroutines.append(coroutine)
        column += 5

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


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    while True:
        curses.wrapper(draw)
