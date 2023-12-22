'''
https://adventofcode.com/2023/day/13
'''
import multiprocessing
import os
from time import perf_counter

day14_input = os.path.join(os.getcwd(), 'day14.txt')


def read_input():
    '''formats the day14.txt'''


def solve_part_one():
    return 0


def solve_part_two():
    return 0


if __name__ == '__main__':
    start_time = perf_counter()
    one_result = solve_part_one()
    one_time = perf_counter() - start_time
    print('Result:', one_result)
    print('Time:', one_time)
    start_time = perf_counter()
    two_result = solve_part_two()
    two_time = perf_counter() - start_time
    print('Result:', two_result)
    print('Time:', two_time)
