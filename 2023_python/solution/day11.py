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
from itertools import combinations
from os.path import dirname, join
from dataclasses import dataclass


@dataclass
class Galaxy:
    '''2D point'''
    x: int
    y: int


def read_input(file_path: str) -> list[list[str]]:
    '''formats the day11.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
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


def expand_rows_theory(universe: list[list[str]]) -> list[int]:
    '''check which rows to expand'''
    expanding_rows = []
    for y_index in range(0, len(universe), 1):
        expand = True
        for char in universe[y_index]:
            if char == '#':
                expand = False
                break
        if expand:
            expanding_rows.append(y_index)
    return expanding_rows


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


def expand_cols_theory(universe: list[list[str]]) -> list[int]:
    '''check which cols to expand'''
    expanding_columns = []
    x_index = 0
    while True:
        if x_index == len(universe[0]):
            break
        expand = True
        for row in universe:
            if row[x_index] == '#':
                expand = False
        if expand:
            expanding_columns.append(x_index)
        x_index += 1
    return expanding_columns


def expand_universe(universe: list[list[str]]):
    '''
    expands the universe
    only some space expands
    any rows or columns that contain no galaxies
    should all actually be twice as big
    '''
    expand_cols(universe)
    expand_rows(universe)


def get_galaxies(universe: list[list[str]]) -> list[Galaxy]:
    '''returns a list of galaxies'''
    galaxies = []
    for y_index in range(0, len(universe), 1):
        for x_index in range(0, len(universe[y_index]), 1):
            if universe[y_index][x_index] == '#':
                galaxies.append(Galaxy(x=x_index, y=y_index))
    return galaxies


def old_get_galaxy_pairs_add_remove(universe: list[list[str]]) -> list[tuple[Galaxy, Galaxy]]:
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


def old_get_galaxy_pairs_check(universe: list[list[str]]) -> list[tuple[Galaxy, Galaxy]]:
    '''returns a list of pairs'''
    galaxies = get_galaxies(universe)
    galaxy_pairs = []
    for first_galaxy in galaxies:
        for second_galaxy in galaxies:
            if not first_galaxy == second_galaxy:
                if (first_galaxy, second_galaxy) not in galaxy_pairs and \
                        (second_galaxy, first_galaxy) not in galaxy_pairs:
                    galaxy_pairs.append((first_galaxy, second_galaxy))
    return galaxy_pairs


def get_galaxy_pairs(galaxies: list[Galaxy]) -> list[tuple[Galaxy, Galaxy]]:
    '''returns a list of pairs'''
    # this is why you shouldnt reinvent the wheel
    return list(combinations(galaxies, 2))


def get_shortest_path(pair: tuple[Galaxy, Galaxy]):
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


def solve_part_one(universe):
    '''solves part one of day 11'''
    expand_universe(universe)
    galaxies = get_galaxies(universe)
    pairs = get_galaxy_pairs(galaxies)
    shortest_paths = []
    for pair in pairs:
        shortest_paths.append(get_shortest_path(pair))
    return sum(shortest_paths)


def solve_part_two(universe):
    '''solves part two of day 11'''
    # instead of expanding, modify the points of galaxies
    galaxies = get_galaxies(universe)
    expanding_columns = expand_cols_theory(universe)
    expanding_rows = expand_rows_theory(universe)
    for galaxy in galaxies:
        # modify the point based on the "theoretical expansion"
        # to do that i need to know:
        # x/y position of galaxy, amount of expansions happening on x/y
        diff_x = 0
        diff_y = 0
        for col in expanding_columns:
            if galaxy.x > col:
                diff_x += 1000000 - 1
        galaxies[galaxies.index(galaxy)].x += diff_x
        for row in expanding_rows:
            if galaxy.y > row:
                diff_y += 1000000 - 1
        galaxies[galaxies.index(galaxy)].y += diff_y
    pairs = get_galaxy_pairs(galaxies)
    shortest_paths = []
    for pair in pairs:
        shortest_paths.append(get_shortest_path(pair))
    return sum(shortest_paths)


if __name__ == '__main__':
    print('Day 11:')
    day11_input = join(dirname(dirname(__file__)), 'input', 'day11.input')
    day11_universe = read_input(day11_input)
    print(f'part one: {solve_part_one(day11_universe)}')
    day11_universe = read_input(day11_input)
    print(f'part two: {solve_part_two(day11_universe)}')
