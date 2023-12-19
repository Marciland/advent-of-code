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
    temp = splits.copy()
    for sp in temp:
        # there are no ? in a sequence of #
        if '?' in sp:
            continue
        # the length fits exactly once
        if numbers.count(len(sp)) == 1:
            splits.remove(sp)
            numbers.remove(len(sp))
    temp = splits.copy()
    for sp in temp:
        # do not change if there is not enough splits
        if len(numbers) != len(splits):
            continue
        # the sequence is found excatly once>
        if numbers.count(len(sp)) == 1:
            splits.remove(sp)
            numbers.remove(len(sp))


def get_possible_arrangements(springs: str, numbers: list[int]) -> int:
    '''get possible arrangements of damaged springs'''
    splits = [x for x in springs.split('.') if x]
    remove_obvious_arrangements(splits, numbers)
    # find possible arrangements
    return 0


def solve_part_one():
    '''solve part one, needs the sum of possible arrangements'''
    springs, numbers = read_input()
    assert len(springs) == len(numbers)
    possible_arrangements = []
    for i in range(0, len(springs), 1):
        possible_arrangements.append(
            get_possible_arrangements(springs[i], numbers[i]))
    print(get_sum(possible_arrangements))


if __name__ == '__main__':
    solve_part_one()
