'''
https://adventofcode.com/2023/day/13

The rounded rocks (O) will roll when the platform is tilted,
while the cube-shaped rocks (#) will stay in place.
empty spaces (.)

Start by tilting the lever so all of the rocks will slide north as far as they will go:
The amount of load caused by a single rounded rock (O) is equal to
the number of rows from the rock to the south edge of the platform,

Cube-shaped rocks (#) don't contribute to load.

Tilt the platform so that the rounded rocks all roll north.
Afterward, what is the total load on the north support beams?
'''
import os
from time import perf_counter


def read_input(file_path: str) -> list[str]:
    '''formats the day14.txt'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        rows = [line.strip() for line in file_handle.readlines()]
    cols = []
    for x_index in range(0, len(rows[0]), 1):
        col = []
        for y_index in range(0, len(rows), 1):
            col.append(rows[y_index][x_index])
        cols.append(''.join(col))
    return cols


def find_free_slot(col: str, start_index: int) -> int:
    '''free_slot is where the next rock could be pushed'''
    free_slot = start_index
    for y_index in range(start_index, len(col), 1):
        if col[y_index] == '.':
            break
        free_slot += 1
    return free_slot


def push_north(col: str) -> str:
    '''move all (moveable) rocks "O" as north as possible'''
    col = list(col)
    next_slot = find_free_slot(col, 0)
    for y_index, symbol in enumerate(col):
        if y_index < next_slot:
            continue
        if symbol == '.':
            continue
        if symbol == 'O':
            col[next_slot] = 'O'
            col[y_index] = '.'
            next_slot = find_free_slot(col, next_slot)
            continue
        if symbol == '#':
            next_slot = find_free_slot(col, y_index)
            continue
    col = ''.join(col)
    return col


def get_load(col: str) -> int:
    '''load is the distance from O to south'''
    total_load = 0
    for y_index, symbol in enumerate(col):
        if symbol == 'O':
            total_load += len(col) - y_index
    return total_load


def solve_part_one(cols: list[str]) -> int:
    '''push all O to north (y-index=0), then return the total load'''
    pushed_cols = [push_north(col) for col in cols]
    print(sum(get_load(col) for col in pushed_cols))


def solve_part_two():
    print('WIP')


def solve():
    print('Day 14:')
    day14_input = os.path.join(os.getcwd(), 'input', 'day14.txt')
    print('part one: ', end='')
    start_time = perf_counter()
    cols = read_input(day14_input)
    solve_part_one(cols)
    print('solved in:', perf_counter() - start_time)
    print('part two: ', end='')
    start_time = perf_counter()
    cols = read_input(day14_input)
    solve_part_two()
    print('solved in:', perf_counter() - start_time)
