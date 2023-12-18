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
import copy
import os
from itertools import combinations

from helpers import Point, get_sum

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


def old_get_galaxy_pairs_add_remove(universe: list[list[str]]) -> list[tuple[Point, Point]]:
    '''returns a list of pairs'''
    galaxies = get_galaxies(universe)
    galaxy_pairs = []
    for first_galaxy in galaxies:
        for second_galaxy in galaxies:
            if not first_galaxy == second_galaxy:
                galaxy_pairs.append((first_galaxy, second_galaxy))
    removed_pairs = []
    temp = galaxy_pairs.copy()
    for temp_pair in temp:
        for pair in temp:
            if temp_pair[0] == pair[1] and temp_pair[1] == pair[0]:
                if not pair in removed_pairs and not temp_pair in removed_pairs:
                    galaxy_pairs.remove(pair)
                    removed_pairs.append(pair)
    return galaxy_pairs


def old_get_galaxy_pairs_check(universe: list[list[str]]) -> list[tuple[Point, Point]]:
    '''returns a list of pairs'''
    galaxies = get_galaxies(universe)
    galaxy_pairs = []
    for first_galaxy in galaxies:
        for second_galaxy in galaxies:
            if not first_galaxy == second_galaxy:
                if (first_galaxy, second_galaxy) not in galaxy_pairs and (second_galaxy, first_galaxy) not in galaxy_pairs:
                    galaxy_pairs.append((first_galaxy, second_galaxy))
    return galaxy_pairs


def get_galaxy_pairs(universe: list[list[str]]) -> list[tuple[Point, Point]]:
    '''returns a list of pairs'''
    galaxies = get_galaxies(universe)
    # this is why you shouldnt reinvent the wheel
    return list(combinations(galaxies, 2))


def get_shortest_path(pair: tuple[Point, Point]):
    '''returns the shortest path between the given pair'''
    first_point = pair[0]
    second_point = pair[1]
    distance = 0
    if first_point.x > second_point.x:
        distance += first_point.x - second_point.x
    else:
        distance += second_point.x - first_point.x
    if first_point.y > second_point.y:
        distance += first_point.y - second_point.y
    else:
        distance += second_point.y - first_point.y
    return distance


def solve_part_one():
    '''solves part one of day 11'''
    universe = read_input()
    expand_universe(universe)
    pairs = get_galaxy_pairs(universe)
    shortest_paths = []
    for pair in pairs:
        shortest_paths.append(get_shortest_path(pair))
    print(get_sum(shortest_paths))


if __name__ == '__main__':
    solve_part_one()
