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


def read_input() -> tuple[list[str], list[int]]:
    '''formats the day12.txt'''
    return ([''], [0])


def get_arrangements(springs: list[str], numbers: list[int]) -> list[int]:
    '''get possible arrangements of damaged springs'''
    return [0]


def solve_part_one():
    '''solve part one, needs the sum of arrangements'''
    springs, numbers = read_input()
    possible_arrangements = get_arrangements(springs, numbers)
    print(get_sum(possible_arrangements))


if __name__ == '__main__':
    solve_part_one()
