import asyncio
import curses
import time


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    row, column = (5, 20)
    coroutine = blink(canvas=canvas, row=row, column=column)

    coroutine.send(None)
    canvas.refresh()
    time.sleep(2)

    coroutine.send(None)
    canvas.refresh()
    time.sleep(0.3)

    coroutine.send(None)
    canvas.refresh()
    time.sleep(0.5)

    coroutine.send(None)
    canvas.refresh()
    time.sleep(0.3)

    time.sleep(10)


def render_flickering_star(canvas):
    canvas.border()
    curses.curs_set(False)
    row, column = (5, 20)
    star = '*'
    canvas.addstr(row, column, star, curses.A_DIM)
    canvas.refresh()
    time.sleep(2)
    canvas.addstr(row, column, star)
    canvas.refresh()
    time.sleep(0.3)
    canvas.addstr(row, column, star, curses.A_BOLD)
    canvas.refresh()
    time.sleep(0.5)
    canvas.addstr(row, column, star)
    canvas.refresh()
    time.sleep(0.3)


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
