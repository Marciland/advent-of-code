'''https://adventofcode.com/2023/day/3'''
from os.path import dirname, join


def read_input(file_path: str) -> list[str]:
    '''formats the day3.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        return [line.strip() for line in file_handle.readlines()]


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


def has_symbol(previous_line: str | None, next_line: str | None, current_line: str,
               start_index: int, number: str) -> bool:
    '''checks at index of prev/next/current if any symbol is adjacent'''
    if previous_line:
        if start_index == 0:
            for radius in range(len(number)+1):
                if previous_line[start_index+radius] != '.' and \
                        not previous_line[start_index+radius].isdigit():
                    return True
        elif start_index + len(number) == len(current_line):
            for radius in range(-1, len(number)):
                if previous_line[start_index+radius] != '.' and \
                        not previous_line[start_index+radius].isdigit():
                    return True
        else:
            for radius in range(-1, len(number)+1):
                if previous_line[start_index+radius] != '.' and \
                        not previous_line[start_index+radius].isdigit():
                    return True
    if next_line:
        if start_index == 0:
            for radius in range(len(number)+1):
                if next_line[start_index+radius] != '.' and \
                        not next_line[start_index+radius].isdigit():
                    return True
        elif start_index + len(number) == len(current_line):
            for radius in range(-1, len(number)):
                if next_line[start_index+radius] != '.' and \
                        not next_line[start_index+radius].isdigit():
                    return True
        else:
            for radius in range(-1, len(number)+1):
                if next_line[start_index+radius] != '.' and \
                        not next_line[start_index+radius].isdigit():
                    return True
    if start_index == 0:
        for radius in range(len(number)+1):
            if current_line[start_index+radius] != '.' and \
                    not current_line[start_index+radius].isdigit():
                return True
    elif start_index + len(number) == len(current_line):
        for radius in range(-1, len(number)):
            if current_line[start_index+radius] != '.' and \
                    not current_line[start_index+radius].isdigit():
                return True
    else:
        for radius in range(-1, len(number)+1):
            if current_line[start_index+radius] != '.' and \
                    not current_line[start_index+radius].isdigit():
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


def check_asterisk(line_index: int, previous_line: str | None, next_line: str | None,
                   current_line: str, start_index: int, number: str) -> tuple[bool, int, int]:
    '''returns match, X, Y'''
    if previous_line:
        if start_index == 0:
            for radius in range(len(number)+1):
                if previous_line[start_index+radius] == '*':
                    return (True, start_index+radius, line_index-1)
        elif start_index + len(number) == len(current_line):
            for radius in range(-1, len(number)):
                if previous_line[start_index+radius] == '*':
                    return (True, start_index+radius, line_index-1)
        else:
            for radius in range(-1, len(number)+1):
                if previous_line[start_index+radius] == '*':
                    return (True, start_index+radius, line_index-1)
    if next_line:
        if start_index == 0:
            for radius in range(len(number)+1):
                if next_line[start_index+radius] == '*':
                    return (True, start_index+radius, line_index+1)
        elif start_index + len(number) == len(current_line):
            for radius in range(-1, len(number)):
                if next_line[start_index+radius] == '*':
                    return (True, start_index+radius, line_index+1)
        else:
            for radius in range(-1, len(number)+1):
                if next_line[start_index+radius] == '*':
                    return (True, start_index+radius, line_index+1)
    if start_index == 0:
        for radius in range(len(number)+1):
            if current_line[start_index+radius] == '*':
                return (True, start_index+radius, line_index)
    elif start_index + len(number) == len(current_line):
        for radius in range(-1, len(number)):
            if current_line[start_index+radius] == '*':
                return (True, start_index+radius, line_index)
    else:
        for radius in range(-1, len(number)+1):
            if current_line[start_index+radius] == '*':
                return (True, start_index+radius, line_index)
    return (False, None, None)


def get_gear_numbers(lines: list[str]) -> list[dict[int, int, str]]:
    '''get * adjacent to part_numbers'''
    gear_numbers = []
    nums_with_index = []
    for line in lines:
        nums_with_index.append(get_numbers_with_index(line))
    for index in range(0, len(lines), 1):
        if index == 0:
            previous_line = None
            next_line = lines[index+1]
            ###
            for start_index, number in nums_with_index[index].items():
                has_asterisk, inline_index, line_index = check_asterisk(
                    index, previous_line, next_line, lines[index], start_index, number)
                if has_asterisk:
                    gear_numbers.append(
                        {'X': inline_index, 'Y': line_index, 'NR': number})
            continue
        if index == len(lines)-1:
            previous_line = lines[index-1]
            next_line = None
            for start_index, number in nums_with_index[index].items():
                has_asterisk, inline_index, line_index = check_asterisk(
                    index, previous_line, next_line, lines[index], start_index, number)
                if has_asterisk:
                    gear_numbers.append(
                        {'X': inline_index, 'Y': line_index, 'NR': number})
            continue
        previous_line = lines[index-1]
        next_line = lines[index+1]
        for start_index, number in nums_with_index[index].items():
            has_asterisk, inline_index, line_index = check_asterisk(
                index, previous_line, next_line, lines[index], start_index, number)
            if has_asterisk:
                gear_numbers.append(
                    {'X': inline_index, 'Y': line_index, 'NR': number})
    return gear_numbers


def get_gear_ratios(gear_numbers: list[dict[int, int, str]]) -> list[int]:
    '''
    look for same index. if EXACTLY 2 hits = gear
    multiply those two for the gear ratio
    '''
    gear_ratios = []
    while True:
        matched_numbers = []
        if not gear_numbers:
            break
        gear_number = gear_numbers.pop()
        matched_numbers.append(gear_number['NR'])
        for possible_match in gear_numbers:
            if gear_number['X'] == possible_match['X']:
                if gear_number['Y'] == possible_match['Y']:
                    matched_numbers.append(possible_match['NR'])
        if len(matched_numbers) == 2:
            gear_ratios.append(int(matched_numbers[0])*int(matched_numbers[1]))
    return gear_ratios


def solve_part_one(lines: list[str]):
    return sum(get_part_numbers(lines))


def solve_part_two(lines: list[str]):
    return sum(get_gear_ratios(get_gear_numbers(lines)))


if __name__ == '__main__':
    print('Day 3:')
    day3_input = join(dirname(dirname(__file__)), 'input', 'day3.input')
    day3_lines = read_input(day3_input)
    print(f'part one: {solve_part_one(day3_lines)}')
    day3_lines = read_input(day3_input)
    print(f'part two: {solve_part_two(day3_lines)}')
