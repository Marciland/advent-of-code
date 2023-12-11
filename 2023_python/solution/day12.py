'''
https://adventofcode.com/2023/day/12
lava shortage
operational (.) or damaged (#) or unknown (?)
nonogram -> contiguous group of damaged

find sum of possible arrangements
'''
import multiprocessing
from itertools import product
from os.path import dirname, join


def read_input(file_path: str) -> tuple[list[str], list[list[int]]]:
    '''formats the day12.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        file_content = [line.strip() for line in file_handle.readlines()]
    springs = [line.split(' ')[0] for line in file_content]
    numbers = [[int(number) for number in line.split(' ')[1].split(',')]
               for line in file_content]
    return springs, numbers


def is_possible(arrangement: str, numbers: list[int]) -> bool:
    splits = [x for x in arrangement.split('.') if x]
    if len(splits) != len(numbers):
        return False
    return all(len(sp) == number for sp, number in zip(splits, numbers))


def generate_possibilities_new(springs: str, numbers: list[int]) -> set:
    possibilities = set()
    defect_springs = springs.count('#')
    expected_defected = sum(numbers)
    for arrangement in product('.#', repeat=springs.count('?')):
        if arrangement.count('#') + defect_springs != expected_defected:
            continue
        possible_springs = iter(arrangement)
        new_springs = ''.join(s if s != '?' else next(
            possible_springs) for s in springs)
        if is_possible(new_springs, numbers):
            possibilities.add(new_springs)
    return possibilities


def solve_part_one_new(springs, numbers):
    '''solve part one, needs the sum of possible arrangements'''
    assert len(springs) == len(numbers)
    starmap = []
    for i in range(0, len(springs), 1):
        starmap.append((springs[i], numbers[i]))
    with multiprocessing.Pool() as pool:
        possible_arrangements = pool.starmap(get_possible_arrangements_new,
                                             starmap)
    return sum(possible_arrangements)


def fill_obvious_defected(springs: str):
    '''if only 1 number is searched and there are split #, fill in middle'''
    start = springs.find('#')
    end = springs.rfind('#')
    if start != -1 and end != -1 and end > start:
        springs = springs[:start] + '#' * (end - start) + springs[end:]
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
            if len(splits[-1]) == numbers[-1] + 1:
                if splits[-1].count('#') == numbers[-1]:
                    print('1\n', splits, numbers, splits[-1], numbers[-1])
                    del splits[-1]
                    del numbers[-1]
                    continue
        if splits[0][0] == '#':
            print('2\n', splits, numbers, splits[0], numbers[0])
            if len(splits[0][numbers[0]+1:]) == 0:
                del splits[0]
            else:
                splits[0] = splits[0][numbers[0]+1:]
            del numbers[0]
            continue
        if splits[-1][-1] == '#':
            print('3\n', splits, numbers, splits[-1], numbers[-1])
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
            print('4\n', splits, numbers, splits[0], numbers[0])
            del splits[0]
            del numbers[0]
            continue
        if len(splits[-1]) == numbers[-1] and '?' not in splits[-1]:
            print('5\n', splits, numbers, splits[-1], numbers[-1])
            del splits[-1]
            del numbers[-1]
            continue
        if len(splits[0]) < numbers[0]:
            print('6\n', splits, numbers, splits[0])
            del splits[0]
            continue
        if len(splits[-1]) < numbers[-1]:
            print('7\n', splits, numbers, splits[-1])
            del splits[-1]
            continue
        if len(numbers) == len(splits) == 1:
            if len(splits[0]) == numbers[0]:
                print('8\n', splits, numbers, splits[0], numbers[0])
                del splits[0]
                del numbers[0]
                continue
        if len(splits) == len(numbers):
            for i, sp in enumerate(splits):
                if sp.count('#') == numbers[i]:
                    if len(sp) == numbers[i] + 1:
                        print('9\n', splits, numbers, splits[i], numbers[i])
                        del splits[i]
                        del numbers[i]
                        continue
        for i, sp in enumerate(splits):
            if sum(len(x) for x in splits) == sum(numbers):
                return [], []
        idle = True
    springs = '.'.join(splits)
    if len(numbers) == 1 and '#' in springs:
        springs = fill_obvious_defected(springs)
        if springs.count('#') == numbers[0]:
            return [], []
    return springs, numbers


def get_possible_arrangements_new(springs: str, numbers: list[int]) -> int:
    springs, numbers = remove_obvious(springs, numbers)
    if len(springs) == len(numbers) == 0:
        # print('hit 1')
        return 1
    if len(springs) == sum(numbers) + len(numbers) - 1:
        # print('hit 2')
        return 1
    if len(numbers) == 1:
        if numbers[0] + 1 == len(springs):
            # print('hit 3')
            return 2
    if '?' in springs:
        all_possibilities = generate_possibilities_new(springs, numbers)
        return sum(1 for _ in all_possibilities)
    return 1


def get_possible_arrangements_two(springs: str, numbers: list[int]) -> int:
    if len(springs) == len(numbers) == 0:
        # print('hit 1')
        return 1
    if len(springs) == sum(numbers) + len(numbers) - 1:
        # print('hit 2')
        return 1
    if len(numbers) == 1:
        if numbers[0] + 1 == len(springs):
            # print('hit 3')
            return 2
    if '?' in springs:
        all_possibilities = generate_possibilities_new(springs, numbers)
        return sum(1 for _ in all_possibilities)
    return 1


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


def solve_part_two(springs, numbers):
    '''solve part two, unfolding: 5 times the original'''
    assert len(springs) == len(numbers)
    springs, numbers = unfold(springs, numbers)
    starmap = []
    for i in range(0, len(springs), 1):
        starmap.append((springs[i], numbers[i]))
    with multiprocessing.Pool() as pool:
        possible_arrangements = pool.starmap(get_possible_arrangements_two,
                                             starmap)
    return sum(possible_arrangements)


if __name__ == '__main__':
    print('Day 12:')
    day12_input = join(dirname(dirname(__file__)), 'input', 'day12.input')
    day12_springs, day12_numbers = read_input(day12_input)
    print(f'part one: {solve_part_one_new(day12_springs, day12_numbers)}')
    day12_springs, day12_numbers = read_input(day12_input)
    print(f'part two: {solve_part_two(day12_springs, day12_numbers)}')
