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
from time import perf_counter

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
    if start and end:
        if end > start:
            springs = springs[:start] + '#' * (end-start) + springs[end:]
    return springs


def remove_obvious(springs: str, numbers: list[int]):
    splits = [x for x in springs.split('.') if x]
    idle = False
    while True:
        if len(splits) == 0 or len(numbers) == 0:
            break
        if idle:
            break
        if len(splits) == len(numbers):
            for i, sp in enumerate(splits):
                if '?' in sp:
                    continue
                if len(sp) == numbers[i]:
                    del splits[i]
                    del numbers[i]
                    continue
        if splits[0][0] == '#':
            if len(splits[0][numbers[0]+1:]) == 0:
                del splits[0]
            else:
                splits[0] = splits[0][numbers[0]+1:]
            del numbers[0]
            continue
        if splits[-1][-1] == '#':
            if len(splits[-1][:-numbers[-1]]) == 0:
                del splits[-1]
            else:
                if splits[-1][:-numbers[-1]-1] != '':
                    splits[-1] = splits[-1][:-numbers[-1]-1]
                else:
                    del splits[-1]
            del numbers[-1]
            continue
        if len(splits[0]) == numbers[0] and '?' not in splits[0]:
            del splits[0]
            del numbers[0]
            continue
        if len(splits[-1]) == numbers[-1] and '?' not in splits[-1]:
            del splits[-1]
            del numbers[-1]
            continue
        if len(splits[0]) < numbers[0]:
            del splits[0]
            continue
        if len(splits[-1]) < numbers[-1]:
            del splits[-1]
            continue
        idle = True
    springs = '.'.join(splits)
    if len(numbers) == 1:
        springs = fill_obvious_defected(springs)
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
    if '?' in springs:
        all_possibilities = generate_possibilities(springs, numbers)
        return sum(1 for _ in all_possibilities)
    return 1


def get_possible_arrangements_new(springs: str, numbers: list[int]) -> int:
    springs, numbers = remove_obvious(springs, numbers)
    if len(springs) == len(numbers) == 0:
        return 1
    if len(springs) == sum(numbers) + len(numbers) - 1:
        return 1
    if len(numbers) == 1 and len(springs) + 1 == numbers[0]:
        return 2
    if '?' in springs:
        all_possibilities = generate_possibilities(springs, numbers)
        return sum(1 for _ in all_possibilities)
    return 1


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
    return get_sum(possible_arrangements)


def solve_part_one_new():
    '''solve part one, needs the sum of possible arrangements'''
    springs, numbers = read_input()
    assert len(springs) == len(numbers)
    starmap = []
    for i in range(0, len(springs), 1):
        starmap.append((springs[i], numbers[i]))
    with multiprocessing.Pool() as pool:
        possible_arrangements = pool.starmap(get_possible_arrangements_new,
                                             starmap)
    return get_sum(possible_arrangements)


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
        unfolded_numbers.append([int(x) for x in
                                 ((number + ',') * 4 + number).split(',')])
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
        possible_arrangements = pool.starmap(get_possible_arrangements_new,
                                             starmap)
    print(get_sum(possible_arrangements))


if __name__ == '__main__':
    start_timer = perf_counter()
    old = solve_part_one()
    old_time = perf_counter()-start_timer
    print('solved part one in:', old_time)
    start_timer = perf_counter()
    new = solve_part_one_new()
    new_time = perf_counter()-start_timer
    print('solved part one new in:', new_time)
    print('old == new ==', new)
    assert old == new
    assert old_time > new_time
    start_timer = perf_counter()
    solve_part_two()
    print('solved part two in:', perf_counter()-start_timer)
