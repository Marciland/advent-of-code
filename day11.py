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


def expand_universe(universe: list[list[str]]):
    '''
    expands the universe
    only some space expands
    any rows or columns that contain no galaxies
    should all actually be twice as big
    '''


def get_galaxy_pairs(universe: list[list[str]]) -> list[tuple[Point, Point]]:
    '''returns a list of pairs'''
    return (Point(x=1, y=2), Point(x=1, y=2))


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
