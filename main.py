"""Module for running main logic of program."""
import curses
import random
import time
from pathlib import PurePath, Path

from async_animations import fire, blink, animate_spaceship, fly_garbage, sleep
from curses_tools import get_frame_size, get_frames
from game_constants import (
    TIC_TIMEOUT, STARS_AMOUNT, STARS_SYMBOLS, BORDER_THICKNESS, START_RANDINT, DIM_DURATION, FRAME_RATE,
)


async def fill_orbit_with_garbage(frames, canvas, columns_number):
    while True:
        for frame in frames:
            _, frame_columns = get_frame_size(frame)
            column = random.randint(START_RANDINT, columns_number - frame_columns - BORDER_THICKNESS)
            coroutines.append(fly_garbage(canvas=canvas, frame=frame, column=column))
            await sleep(tics=FRAME_RATE)


def draw(canvas) -> None:
    """
    This function like event loop, use for register and running tasks.
    param canvas: place for render all animation.
    """
    canvas.border()
    curses.curs_set(False)
    rows_number, columns_number = canvas.getmaxyx()  # Return a tuple (y, x) of the height and width of the window.
    abs_base_path = Path('frames').absolute()
    spaceship_path = PurePath.joinpath(abs_base_path, 'rocket')
    garbage_path = PurePath.joinpath(abs_base_path, 'garbage')

    for star in range(STARS_AMOUNT):
        row = random.randint(0, rows_number - BORDER_THICKNESS)
        column = random.randint(START_RANDINT, columns_number - BORDER_THICKNESS)
        coroutine = blink(
            canvas=canvas, row=row, column=column, symbol=random.choice(STARS_SYMBOLS),
            offset_tics=random.randint(START_RANDINT, DIM_DURATION),
        )
        coroutines.append(coroutine)

    spaceship_frames = get_frames(path=spaceship_path)
    garbage_frames = get_frames(path=garbage_path)

    fire_coroutine = fire(
        canvas=canvas, start_row=rows_number - BORDER_THICKNESS,
        start_column=columns_number - BORDER_THICKNESS, rows_speed=-1,
    )
    spaceship_coroutine = animate_spaceship(
        canvas=canvas, row=rows_number // 2, column=columns_number // 2,
        rows_number=rows_number, columns_number=columns_number, frames=spaceship_frames,
    )
    garbage_coroutine = fill_orbit_with_garbage(canvas=canvas, frames=garbage_frames, columns_number=columns_number)
    coroutines.extend([fire_coroutine, spaceship_coroutine, garbage_coroutine])

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
    coroutines = []
    curses.update_lines_cols()
    curses.wrapper(draw)
