'''https://adventofcode.com/2023/day/18'''
from os.path import dirname, join
from time import perf_counter

from helpers import Point


def read_input_one(file_path: str) -> tuple[str, int]:
    '''formats the day18.txt'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        # colors are not needed for part one
        return [(line.split(' ')[0], int(line.split(' ')[1]))
                for line in file_handle.readlines()]


def layout_trench(instructions: tuple[str, int]) -> set[Point]:
    '''up (U), down (D), left (L), or right (R)'''
    right = Point(x=1, y=0)
    left = Point(x=-1, y=0)
    up = Point(x=0, y=-1)
    down = Point(x=0, y=1)
    trench = set()
    start_position = Point(x=0, y=0)
    trench.add(start_position)
    current_position = start_position
    for instruction in instructions:
        for _ in range(instruction[1]):
            if instruction[0] == 'R':
                current_position = current_position.add(right)
                trench.add(current_position)
            if instruction[0] == 'L':
                current_position = current_position.add(left)
                trench.add(current_position)
            if instruction[0] == 'D':
                current_position = current_position.add(down)
                trench.add(current_position)
            if instruction[0] == 'U':
                current_position = current_position.add(up)
                trench.add(current_position)
    return trench


def solve_part_one(instructions: tuple[str, int]):
    '''digging a lagoon to store lava, how much is dug out?
    R 6 (#70c710)
    D 5 (#0dc571)
    L 2 (#5713f0)
    D 2 (#d2c081)
    R 2 (#59c680)
    D 2 (#411b91)
    L 5 (#8ceee2)
    U 2 (#caa173)
    L 1 (#1b58a2)
    U 2 (#caa171)
    R 2 (#7807d2)
    U 3 (#a77fa3)
    L 2 (#015232)
    U 2 (#7a21e3)

    -> 38
    -> 62 with interior
    '''
    trench = layout_trench(instructions)
    # fill the interior of the trench with ray casting


def solve_part_two():
    pass


def solve():
    print('Day 18:')
    day18_input = join(dirname(dirname(__file__)), 'input', 'day18.txt')
    print('part one: ', end='')
    start_time = perf_counter()
    instructions = read_input_one(day18_input)
    solve_part_one(instructions)
    print('solved in:', perf_counter() - start_time)
    print('part two: ', end='')
    start_time = perf_counter()
    # read_input(day18_input)
    solve_part_two()
    print('solved in:', perf_counter() - start_time)
