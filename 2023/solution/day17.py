'''https://adventofcode.com/2023/day/17'''
from os.path import dirname, join
from time import perf_counter


def read_input(file_path: str):
    '''formats the day17.txt'''


def solve_part_one():
    '''
    minimize heat loss
    amount of heat loss if the crucible enters that block
    starting point: top-left city block
    destination: bottom-right city block
    (Because you already start in the top-left block, you don't incur that block's heat loss)
    at most three blocks (single direction) before it must turn 90 degrees left or right
    what is the least heat loss it can incur?
    '''
    print('WIP')
    # collect heat loss on the way, sum it up
    # compare different routes and return the smallest sum


def solve_part_two():
    print('WIP')


def solve():
    print('Day 17:')
    day17_input = join(dirname(dirname(__file__)), 'input', 'day17.txt')
    print('part one: ', end='')
    start_time = perf_counter()
    read_input(day17_input)
    solve_part_one()
    print('solved in:', perf_counter() - start_time)
    print('part two: ', end='')
    start_time = perf_counter()
    read_input(day17_input)
    solve_part_two()
    print('solved in:', perf_counter() - start_time)
