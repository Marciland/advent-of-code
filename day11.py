'''
https://adventofcode.com/2023/day/11

The image includes:
empty space (.)
and galaxies (#)

sum of the lengths of the shortest path
between every pair of galaxies

only some space expands
any rows or columns that contain no galaxies
should all actually be twice as big

It can help to assign every galaxy a unique number
Only count each pair once
move up, down, left, or right exactly one . or # at a time.

Expand the universe,
then find the length of the shortest path
between every pair of galaxies.
What is the sum of these lengths?
'''
import os
import copy

from helpers import get_sum, Point

day11_input = os.path.join(os.getcwd(), 'day11.txt')


def read_input() -> list[list[str]]:
    '''formats the day11.txt'''
    with open(day11_input, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    lines = []
    for line in file_content:
        lines.append(list(line.strip()))
    return lines


def expand_rows(universe: list[list[str]]):
    '''check which rows to expand'''
    temp = copy.deepcopy(universe)
    inserted = 0
    for y_index in range(0, len(temp), 1):
        expand = True
        for char in temp[y_index]:
            if char == '#':
                expand = False
                break
        if expand:
            universe.insert(y_index+inserted, temp[y_index])
            inserted += 1


def expand_cols(universe: list[list[str]]):
    '''check which cols to expand'''
    temp = copy.deepcopy(universe)
    x_index = 0
    inserted = 0
    while True:
        if x_index == len(temp[0]):
            break
        expand = True
        for row in temp:
            if row[x_index] == '#':
                expand = False
        if expand:
            for row in universe:
                row.insert(x_index + inserted, row[x_index+inserted])
            inserted += 1
        x_index += 1


def expand_universe(universe: list[list[str]]):
    '''
    expands the universe
    only some space expands
    any rows or columns that contain no galaxies
    should all actually be twice as big
    '''
    expand_rows(universe)
    expand_cols(universe)


def get_galaxies(universe: list[list[str]]) -> list[Point]:
    '''returns a list of galaxies'''
    galaxies = []
    for y_index in range(0, len(universe), 1):
        for x_index in range(0, len(universe[y_index]), 1):
            if universe[y_index][x_index] == '#':
                galaxies.append(Point(x=x_index, y=y_index))
    return galaxies


def get_galaxy_pairs(universe: list[list[str]]) -> list[tuple[Point, Point]]:
    '''returns a list of pairs'''
    galaxies = get_galaxies(universe)
    return [(Point(x=1, y=2), Point(x=1, y=2))]


def get_shortest_path(pair: tuple[Point, Point]):
    '''returns the shortest path between the given pair'''


def solve_part_one():
    '''solves part one of day 11'''
    universe = read_input()
    expand_universe(universe)
    pairs = get_galaxy_pairs(universe)
    lengths = []
    for pair in pairs:
        lengths.append(get_shortest_path(pair))
    print(get_sum(lengths))


if __name__ == '__main__':
    solve_part_one()
