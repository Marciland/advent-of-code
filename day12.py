'''
https://adventofcode.com/2023/day/12
lava shortage
operational (.) or damaged (#) or unknown (?)
nonogram -> contiguous group of damaged

find sum of possible arrangements
'''
import multiprocessing
import os
from itertools import product

from helpers import get_sum

day12_input = os.path.join(os.getcwd(), 'day12.txt')


def read_input() -> tuple[list[str], list[list[int]]]:
    '''formats the day12.txt'''
    with open(day12_input, 'r', encoding='utf-8') as file_handle:
        file_content = [line.strip() for line in file_handle.readlines()]
    springs = [line.split(' ')[0] for line in file_content]
    numbers = [[int(number) for number in line.split(' ')[1].split(',')]
               for line in file_content]
    return springs, numbers


def fill_obvious_defected(springs: str):
    '''if only 1 number is searched and there are split #, fill in middle'''
    start, end = None, None
    counter = 0
    for i, char in enumerate(springs):
        if char == '#':
            if counter == 0:
                start = i
            counter += 1
            if counter == springs.count('#'):
                end = i
    if end > start:
        springs = springs[:start] + '#' * (end-start) + springs[end:]
    return springs


def generate_possibilities(springs: str) -> set:
    possibilities = set()
    for arrangement in product('.#', repeat=springs.count('?')):
        possible_springs = iter(arrangement)
        new_springs = ''.join(s if s != '?'
                              else next(possible_springs) for s in springs)
        possibilities.add(new_springs)
    return possibilities


def is_possible(arrangement: str, numbers: list[int]) -> bool:
    splits = [x for x in arrangement.split('.') if x]
    return len(splits) == len(numbers) and all(len(sp) == number for sp, number in zip(splits, numbers))


def get_possible_arrangements(springs: str, numbers: list[int]) -> int:
    if '?' in springs:
        all_possibilities = generate_possibilities(springs)
        return sum(1 for arrangement in all_possibilities if is_possible(arrangement, numbers))
    return None


def solve_part_one():
    '''solve part one, needs the sum of possible arrangements'''
    springs, numbers = read_input()
    assert len(springs) == len(numbers)
    starmap = []
    for i in range(0, len(springs), 1):
        starmap.append((springs[i], numbers[i]))
    with multiprocessing.Pool() as pool:
        possible_arrangements = pool.starmap(get_possible_arrangements,
                                             starmap)
    print(get_sum(possible_arrangements))


if __name__ == '__main__':
    solve_part_one()
