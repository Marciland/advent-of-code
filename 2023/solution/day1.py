'''https://adventofcode.com/2023/day/1'''
import os


def read_input(file_path: str) -> list[str]:
    '''return day1.txt as list of strings'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        return file_handle.readlines()


def get_numbers(text_input: list[str]) -> list[int]:
    '''retrieves first and last number as one number'''
    numbers = []
    for text in text_input:
        number = 0
        last_digit = 0
        for symbol in text:
            if symbol.isnumeric():
                symbol = int(symbol)
                last_digit = symbol
                if number == 0:
                    number += symbol
        number = number*10 + last_digit
        numbers.append(number)
    return numbers


def substitute_written_numbers(text_input: list[str]) -> list[str]:
    '''converts written numbers to numbers'''
    written_numbers = ['one', 'two', 'three', 'four', 'five',
                       'six', 'seven', 'eight', 'nine']
    converted_list = []
    for line in text_input:
        new_line = line
        while True:
            if len(line) == 0:
                break
            lowest_index = None
            for number in written_numbers:
                if number in line:
                    index = line.find(number)
                    if lowest_index is None:
                        lowest_index = index
                    if index < lowest_index:
                        lowest_index = index
            if lowest_index is None:
                break
            if lowest_index != 0:
                line = line[lowest_index:]
            for number in written_numbers:
                if line.startswith(number):
                    value = str(written_numbers.index(number)+1)
                    new_line = new_line[0:new_line.index(
                        number)] + value + new_line[new_line.index(number)+1:]
                    line = line[1:]
        converted_list.append(new_line)
    return converted_list


def solve_part_one(text_list: list[str]):
    print(sum(get_numbers(text_list)))


def solve_part_two(text_list: list[str]):
    print(sum(get_numbers(substitute_written_numbers(text_list))))


def solve():
    print('Day 1:')
    day1_input = os.path.join(os.getcwd(), 'input', 'day1.txt')
    text_list = read_input(day1_input)
    print('part one: ', end='')
    solve_part_one(text_list)
    print('part two: ', end='')
    solve_part_two(text_list)
