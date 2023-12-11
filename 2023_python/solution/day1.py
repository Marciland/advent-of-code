'''https://adventofcode.com/2023/day/1'''
from os.path import dirname, join


def read_input(file_path: str) -> list[str]:
    '''return day1.input as list of strings'''
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
    return sum(get_numbers(text_list))


def solve_part_two(text_list: list[str]):
    return sum(get_numbers(substitute_written_numbers(text_list)))


if __name__ == '__main__':
    print('Day 1:')
    day1_file = join(dirname(dirname(__file__)), 'input', 'day1.input')
    day1_input = read_input(day1_file)
    print(f'part one: {solve_part_one(day1_input)}')
    day1_input = read_input(day1_file)
    print(f'part two: {solve_part_two(day1_input)}')
