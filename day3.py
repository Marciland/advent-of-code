'''https://adventofcode.com/2023/day/3'''
import os

from helpers import get_sum

day3_input = os.path.join(os.getcwd(), 'day3.txt')


def read_input() -> list[str]:
    '''formats the day3.txt'''
    with open(day3_input, 'r', encoding='utf-8') as file_handle:
        return [line.strip() for line in file_handle.readlines()]

# full number + index to have a unique identifier!!!


def get_numbers_with_index(line: str) -> dict[int, str]:
    '''get all numbers with start index from a line'''
    num_with_index = {}
    current_digit = ''
    for index in range(0, len(line), 1):
        if line[index].isdigit():
            current_digit += line[index]
        else:
            if current_digit != '':
                num_with_index.update(
                    {index-len(current_digit): current_digit})
                current_digit = ''
    if current_digit != '':
        num_with_index.update({index-len(current_digit)+1: current_digit})
    return num_with_index

# if only '.' is around a number -> not a part number!


def has_symbol(previous_line: str | None, next_line: str | None, current_line: str, start_index: int, number: str) -> bool:
    '''checks at index of prev/next/current if any symbol is adjacent'''
    if previous_line:
        if start_index == 0:
            for radius in range(len(number)+1):
                if previous_line[start_index+radius] != '.' and not previous_line[start_index+radius].isdigit():
                    return True
        elif start_index + len(number) == len(current_line):
            for radius in range(-1, len(number)):
                if previous_line[start_index+radius] != '.' and not previous_line[start_index+radius].isdigit():
                    return True
        else:
            for radius in range(-1, len(number)+1):
                if previous_line[start_index+radius] != '.' and not previous_line[start_index+radius].isdigit():
                    return True
    if next_line:
        if start_index == 0:
            for radius in range(len(number)+1):
                if next_line[start_index+radius] != '.' and not next_line[start_index+radius].isdigit():
                    return True
        elif start_index + len(number) == len(current_line):
            for radius in range(-1, len(number)):
                if next_line[start_index+radius] != '.' and not next_line[start_index+radius].isdigit():
                    return True
        else:
            for radius in range(-1, len(number)+1):
                if next_line[start_index+radius] != '.' and not next_line[start_index+radius].isdigit():
                    return True
    if start_index == 0:
        for radius in range(len(number)+1):
            if current_line[start_index+radius] != '.' and not current_line[start_index+radius].isdigit():
                return True
    elif start_index + len(number) == len(current_line):
        for radius in range(-1, len(number)):
            if current_line[start_index+radius] != '.' and not current_line[start_index+radius].isdigit():
                return True
    else:
        for radius in range(-1, len(number)+1):
            if current_line[start_index+radius] != '.' and not current_line[start_index+radius].isdigit():
                return True
    return False


def get_part_numbers(lines: list[str]) -> list[int]:
    '''returns all numbers that have an adjacent symbol'''
    part_numbers = []
    nums_with_index = []
    for line in lines:
        nums_with_index.append(get_numbers_with_index(line))
    for index in range(0, len(lines), 1):
        if index == 0:
            previous_line = None
            next_line = lines[index+1]
            for start_index, number in nums_with_index[index].items():
                if has_symbol(previous_line, next_line, lines[index], start_index, number):
                    part_numbers.append(int(number))
            continue
        if index == len(lines)-1:
            previous_line = lines[index-1]
            next_line = None
            for start_index, number in nums_with_index[index].items():
                if has_symbol(previous_line, next_line, lines[index], start_index, number):
                    part_numbers.append(int(number))
            continue
        previous_line = lines[index-1]
        next_line = lines[index+1]
        for start_index, number in nums_with_index[index].items():
            if has_symbol(previous_line, next_line, lines[index], start_index, number):
                part_numbers.append(int(number))
    return part_numbers


print(get_sum(get_part_numbers(read_input())))  # part one
