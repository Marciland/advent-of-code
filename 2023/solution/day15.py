'''https://adventofcode.com/2023/day/15'''
import os
from multiprocessing import Pool
from time import perf_counter


def read_input(file_path: str) -> list[str]:
    '''formats the day15.txt'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        return list(file_handle.readlines()[0].split(','))


def hash_string(string: str) -> int:
    '''ASCII code, *17, modulo 256 for each char'''
    current_value = 0
    for char in list(string):
        current_value += ord(char)
        current_value *= 17
        current_value = current_value % 256
    return current_value


def solve_part_one(strings: list[str]):
    '''determine sum of hashed values for the initialization sequence'''
    with Pool() as pool:
        hashed_values = pool.map(hash_string, strings)
    print(sum(hashed_values))


def solve_part_two():
    print('WIP')


def solve():
    print('Day 15:')
    day15_input = os.path.join(os.getcwd(), 'input', 'day15.txt')
    print('part one: ', end='')
    start_time = perf_counter()
    strings = read_input(day15_input)
    solve_part_one(strings)
    print('solved in:', perf_counter() - start_time)
    print('part two: ', end='')
    start_time = perf_counter()
    strings = read_input(day15_input)
    solve_part_two()
    print('solved in:', perf_counter() - start_time)
