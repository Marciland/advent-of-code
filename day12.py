'''
https://adventofcode.com/2023/day/12
lava shortage
operational (.) or damaged (#) or unknown (?)
nonogram -> contiguous group of damaged

find sum of possible arrangements
'''
import os

from helpers import get_sum

day12_input = os.path.join(os.getcwd(), 'day12.txt')


def read_input() -> tuple[list[str], list[list[int]]]:
    '''formats the day12.txt'''
    with open(day12_input, 'r', encoding='utf-8') as file_handle:
        file_content = [line.strip() for line in file_handle.readlines()]
    springs = [line.split(' ')[0] for line in file_content]
    numbers = [[int(number) for number in line.split(' ')[1].split(',')]
               for line in file_content]
    return (springs, numbers)


def remove_obvious_arrangements(splits: list[str], numbers: list[int]):
    '''obvious if:'''
    len_splits = 0
    len_numbers = get_sum(numbers)
    for sp in splits:
        len_splits += len(sp)
    if len_splits == len_numbers:
        splits.clear()
        numbers.clear()
        return
    idle = False
    while True:
        if idle:
            break
        if len(splits[0]) == numbers[0] and '?' not in splits[0]:
            del splits[0]
            del numbers[0]
            continue
        idle = True
    temp = splits.copy()
    for sp in temp:
        if '?' in sp:
            continue
        if numbers.count(len(sp)) == 1:
            # print('remove', sp, 'from', splits, numbers, 'at', splits.index(sp), numbers.index(len(sp)))
            splits.remove(sp)
            numbers.remove(len(sp))
    if len(splits) == len(numbers) == 0:
        return
    temp = splits.copy()
    for sp in temp:
        if '?' in sp:
            continue
        if len(numbers) != len(splits):
            continue
        if splits.index(sp) == numbers.index(len(sp)):
            # print('remove', sp, 'from', splits, numbers, 'at', splits.index(sp), numbers.index(len(sp)))
            splits.remove(sp)
            numbers.remove(len(sp))
    if len(splits) == len(numbers) == 0:
        return
    temp = splits.copy()
    for sp in temp:
        if len(sp) < 5:
            continue
        if len(numbers) != len(splits):
            continue
        if len(sp) not in numbers:
            continue
        if splits.index(sp) != numbers.index(len(sp)):
            continue
        if numbers.count(len(sp)) == 1:
            # print('remove', sp, 'from', splits, numbers, 'at', splits.index(sp), numbers.index(len(sp)))
            splits.remove(sp)
            numbers.remove(len(sp))
    if len(splits) == len(numbers) == 0:
        return
    temp = splits.copy()
    for sp in temp:
        if sp.count('#') not in numbers:
            continue
        if numbers.count(sp.count('#')) != 1:
            continue
        if len(splits) != len(numbers):
            continue
        if sp.count('?') > numbers[numbers.index(sp.count('#'))]:
            continue
        if '#' * numbers[numbers.index(sp.count('#'))] not in sp:
            continue
        if splits.index(sp) == numbers.index(sp.count('#')):
            # print('remove', sp, 'from', splits, numbers, 'at', splits.index(sp), numbers.index(sp.count('#')))
            splits.remove(sp)
            numbers.remove(sp.count('#'))
    if len(splits) == len(numbers) == 0:
        return
    temp = splits.copy()
    for sp in temp:
        if '?' in sp:
            continue
        if len(numbers) != len(splits):
            continue
        # print('remove', sp, 'from', splits, numbers, 'at', splits.index(sp), numbers[splits.index(sp)])
        del numbers[splits.index(sp)]
        splits.remove(sp)
    if len(splits) == len(numbers) == 0:
        return
    idle = False
    while True:
        if idle:
            break
        if len(splits[0]) < numbers[0]:
            del splits[0]
            continue
        if len(splits[-1]) < numbers[-1]:
            del splits[-1]
            continue
        idle = True
    if len(splits) == len(numbers) == 0:
        return


def get_possible_arrangements(springs: str, numbers: list[int]) -> int:
    '''get possible arrangements of damaged springs'''
    splits = [x for x in springs.split('.') if x]
    remove_obvious_arrangements(splits, numbers)
    if len(splits) == len(numbers) == 0:
        return 1
    # find possible arrangements
    return 0


def solve_part_one():
    '''solve part one, needs the sum of possible arrangements'''
    springs, numbers = read_input()
    assert len(springs) == len(numbers)
    possible_arrangements = []
    for i in range(0, len(springs), 1):
        possible_arrangements.append(get_possible_arrangements(springs[i],
                                                               numbers[i]))
    print(get_sum(possible_arrangements))


if __name__ == '__main__':
    solve_part_one()
