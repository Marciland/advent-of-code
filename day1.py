'''https://adventofcode.com/2023/day/1'''
import os

from helpers import get_sum

day1_input = os.path.join(os.getcwd(), 'day1.txt')
written_numbers = ['one', 'two', 'three', 'four',
                   'five', 'six', 'seven', 'eight', 'nine']


def read_input() -> list[str]:
    '''return day1.txt as list of strings'''
    with open(day1_input, 'r', encoding='utf-8') as file_handle:
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


assert get_numbers(['12383ajhlskgdhaodz12zghbvfdu6234jhl12213']) == [13]


assert get_sum([15, 12, 33, 54]) == 15+12+33+54


def substitute_written_numbers(text_input: list[str]) -> list[str]:
    '''converts written numbers to numbers'''
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


text_list = read_input()

number_list = get_numbers(text_list)
final_sum = get_sum(number_list)
print(final_sum)  # part one

subsituted_text = substitute_written_numbers(text_list)
number_list = get_numbers(subsituted_text)
final_sum = get_sum(number_list)
print(final_sum)  # part two
