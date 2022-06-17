import time
import curses


def draw(canvas):
    row, column = (5, 20)
    canvas.addstr(row, column, 'Hello, World!')
    canvas.refresh()
    curses.curs_set(False)
    canvas.border()
    time.sleep(5)


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


if __name__ == '__main__':
    curses.update_lines_cols()
    while True:
        curses.wrapper(render_flickering_star)
