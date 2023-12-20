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


def remove_obvious(springs: str, numbers: list[int]):
    return springs, numbers


def generate_possibilities(springs: str, numbers: list[int]) -> set:
    possibilities = set()
    for arrangement in product('.#', repeat=springs.count('?')):
        possible_springs = iter(arrangement)
        new_springs = ''.join(s if s != '?'
                              else next(possible_springs) for s in springs)
        if is_possible(new_springs, numbers):
            possibilities.add(new_springs)
    return possibilities


def is_possible(arrangement: str, numbers: list[int]) -> bool:
    splits = [x for x in arrangement.split('.') if x]
    return len(splits) == len(numbers) and all(len(sp) == number for sp, number in zip(splits, numbers))


def get_possible_arrangements(springs: str, numbers: list[int]) -> int:
    springs, numbers = remove_obvious(springs, numbers)
    if '?' in springs:
        all_possibilities = generate_possibilities(springs, numbers)
        print('done with generating possibilities for', springs)
        return sum(1 for _ in all_possibilities)
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


def unfold(springs: list[str], numbers: list[list[int]]):
    '''
    replace the list of springs with five copies of itself (separated by ?)
    replace the list of numbers with five copies of itself (separated by ,)
    .# 1 -> .#?.#?.#?.#?.# 1,1,1,1,1
    '''
    unfolded_springs = []
    for spring in springs:
        unfolded_springs.append((spring + '?') * 4 + spring)
    unfolded_numbers = []
    for number in numbers:
        number = ','.join([str(x) for x in number])
        unfolded_numbers.append((number + ',') * 4 + number)
    return unfolded_springs, unfolded_numbers


def solve_part_two():
    '''solve part two, unfolding: 5 times the original'''
    springs, numbers = read_input()
    assert len(springs) == len(numbers)
    springs, numbers = unfold(springs, numbers)
    starmap = []
    for i in range(0, len(springs), 1):
        starmap.append((springs[i], numbers[i]))
    with multiprocessing.Pool() as pool:
        possible_arrangements = pool.starmap(get_possible_arrangements,
                                             starmap)
    print(get_sum(possible_arrangements))


if __name__ == '__main__':
    solve_part_one()
    solve_part_two()
