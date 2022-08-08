"""Module that helps animate frames."""
import asyncio
import curses
import random
from itertools import cycle

from curses_tools import draw_frame, read_controls, get_frame_size
from game_constants import DIM_DURATION, NORMAL_DURATION, BRIGHT_DURATION, BORDER_THICKNESS, START_RANDINT, FRAME_RATE, \
    CENTRAL_FIRE_OFFSET
from game_engine.explosion import explode
from game_engine.obstacles import Obstacle
from game_engine.physics import update_speed

coroutines = []
obstacles = []
obstacles_in_last_collisions = []


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
        for obstacle in obstacles:
            if obstacle.has_collision(obj_corner_row=row, obj_corner_column=column):
                obstacles_in_last_collisions.append(obstacle)
                return
        else:
            canvas.addstr(round(row), round(column), symbol)
            await asyncio.sleep(0)
            canvas.addstr(round(row), round(column), ' ')
            row += rows_speed
            column += columns_speed


async def animate_spaceship(
        canvas: curses.window,
        rows_number: int, columns_number: int, frames: list, game_over: str,
) -> None:
    """
    Animate spaceship frames.
    :param canvas: place for rendering animation.
    :param rows_number: height of the window.
    :param columns_number: width of the window.
    :param frames: content, that reads from txt file.
    :return: None
    """
    row = rows_number // 2
    column = columns_number // 2

    for frame in cycle(frames):

        for _ in range(2):
            row_speed = column_speed = 0
            rows_direction, columns_direction, space_pressed = read_controls(canvas)
            frame_rows, frame_columns = get_frame_size(frame)

            row = min(row + rows_direction, rows_number - frame_rows - BORDER_THICKNESS)
            row = max(row, BORDER_THICKNESS)
            column = min(column + columns_direction, columns_number - frame_columns - BORDER_THICKNESS)
            column = max(column, BORDER_THICKNESS)
            fire_column = column + CENTRAL_FIRE_OFFSET

            if space_pressed:
                coroutines.append(fire(canvas=canvas, start_row=row, start_column=fire_column, rows_speed=-1))

            row_speed, column_speed = update_speed(
                row_speed=row_speed, column_speed=column_speed, rows_direction=rows_direction,
                columns_direction=columns_direction,
            )

            for obstacle in obstacles:
                if obstacle.has_collision(obj_corner_row=row, obj_corner_column=column):
                    await show_gameover(canvas=canvas, frame=game_over)
                    return

            draw_frame(canvas, row + row_speed, column + column_speed, frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row + row_speed, column + column_speed, frame, negative=True)


async def fly_garbage(canvas, column, frame, rows, columns, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""

    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    obstacle = Obstacle(row=row, column=column, rows_size=rows, columns_size=columns)
    obstacles.append(obstacle)

    while row < rows_number:
        center_row = row + rows // 2
        center_column = column + columns // 2

        for barrier in obstacles_in_last_collisions:
            if barrier.has_collision(obj_corner_row=row, obj_corner_column=column):
                obstacles_in_last_collisions.remove(barrier)
                obstacles.remove(obstacle)
                await explode(canvas, center_row=center_row, center_column=center_column)
                return

        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)
        row += speed
        obstacle.row += speed


async def fill_orbit_with_garbage(frames: list, canvas: curses.window, columns_number: int) -> None:
    """Coroutine that fill orbit with garbage frames chaotically.
    :param frames: spacehip frames.
    :param canvas: place for render all animation.
    :param columns_number: width of the window.
    :return: None
    """
    while True:
        for frame in frames:
            frame_rows, frame_columns = get_frame_size(frame)
            column = random.randint(START_RANDINT, columns_number - frame_columns - BORDER_THICKNESS)
            coroutines.append(fly_garbage(
                canvas=canvas, frame=frame,
                column=column, rows=frame_rows, columns=frame_columns,
            ))
            await sleep(tics=FRAME_RATE)


async def show_gameover(canvas, frame, row=15, column=35):
    while True:
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)


async def sleep(tics):
    """
    Custom sleep for make ping in code.
    :param tics: amount of iterations.
    """
    for _ in range(tics):
        await asyncio.sleep(0)
