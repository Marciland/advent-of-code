'''https://adventofcode.com/2023/day/16'''
import os
from time import perf_counter

from helpers import Point

RIGHT = Point(x=1, y=0)
LEFT = Point(x=-1, y=0)
UP = Point(x=0, y=-1)
DOWN = Point(x=0, y=1)


def read_input(file_path: str) -> dict[Point]:
    '''formats the day16.txt'''
    contraption = {}
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        rows = [line.strip() for line in file_handle.readlines()]
    for y_index, row in enumerate(rows):
        for x_index in range(0, len(row), 1):
            contraption.update({Point(y=y_index, x=x_index): row[x_index]})
    return contraption


def beam_ended(position: Point, max_position: Point) -> bool:
    '''beam ends if it leaves the contraption -> negative or higher than bounds'''
    if position.x < 0:
        return True
    if position.y < 0:
        return True
    if position.x > max_position.x:
        return True
    if position.y > max_position.y:
        return True
    return False


def handle_backslash(current_position: Point,
                     current_direction: Point) -> tuple[Point, Point] | None:
    '''decide where the beam should move on backslash'''
    if current_direction == RIGHT:
        current_direction = DOWN
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == LEFT:
        current_direction = UP
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == UP:
        current_direction = LEFT
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == DOWN:
        current_direction = RIGHT
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    return None


def handle_slash(current_position: Point,
                 current_direction: Point) -> tuple[Point, Point] | None:
    '''decide where the beam should move on slash'''
    if current_direction == RIGHT:
        current_direction = UP
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == LEFT:
        current_direction = DOWN
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == UP:
        current_direction = RIGHT
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == DOWN:
        current_direction = LEFT
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    return None


def handle_minus(current_position: Point,
                 current_direction: Point) -> tuple[Point, Point] | None:
    '''decide where the beam should move on minus'''
    if current_direction == RIGHT:
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == LEFT:
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == UP:
        handle_split()
        # WIP what where to send the beam?
        return current_position, current_direction
    if current_direction == DOWN:
        handle_split()
        # WIP what where to send the beam?
        return current_position, current_direction
    return None


def handle_pipe(current_position: Point,
                current_direction: Point) -> tuple[Point, Point] | None:
    '''decide where the beam should move on pipe'''
    if current_direction == RIGHT:
        handle_split()
        # WIP what where to send the beam?
        return current_position, current_direction
    if current_direction == LEFT:
        handle_split()
        # WIP what where to send the beam?
        return current_position, current_direction
    if current_direction == UP:
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == DOWN:
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    return None


def handle_split():
    # run same logic with another starting point, continue old beam in main?
    # how to count energized?
    pass


def solve_part_one(contraption: dict[Point]) -> int:
    '''
    empty space (.) -> same direction
    mirrors (/ and \) -> reflected
    splitters (| and -) -> pointy end of a splitter: like empty space,
                           flat side of a splitter -> split into two beams
    A tile is energized if that tile has at least one beam
    '''
    current_direction = RIGHT
    current_position = Point(x=0, y=0)
    # sets will not count duplicates when sum is used
    energized = set()
    while True:
        if beam_ended(current_position, list(contraption)[-1]):
            break
        energized.add(current_position)
        if contraption[current_position] == '.':
            current_position = current_position.add(current_direction)
            continue
        if contraption[current_position] == '\\':
            current_position, current_direction = handle_backslash(current_position,
                                                                   current_direction)
            continue
        if contraption[current_position] == '/':
            current_position, current_direction = handle_slash(current_position,
                                                               current_direction)
            continue
        if contraption[current_position] == '-':
            current_position, current_direction = handle_minus(current_position,
                                                               current_direction)
            continue
        if contraption[current_position] == '|':
            current_position, current_direction = handle_pipe(current_position,
                                                              current_direction)
            continue
    print(sum(energized))


def solve_part_two():
    ''''''
    print('WIP')


def solve():
    print('Day 16:')
    day16_input = os.path.join(os.getcwd(), 'input', 'day16.txt')
    print('part one: ', end='')
    start_time = perf_counter()
    contraption = read_input(day16_input)
    solve_part_one(contraption)
    print('solved in:', perf_counter() - start_time)
    print('part two: ', end='')
    start_time = perf_counter()
    contraption = read_input(day16_input)
    solve_part_two()
    print('solved in:', perf_counter() - start_time)
