'''https://adventofcode.com/2023/day/15'''
from multiprocessing import Pool
from os.path import dirname, join


def read_input(file_path: str) -> list[str]:
    '''formats the day15.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        return list(file_handle.readlines()[0].split(','))


def hash_string(string: str) -> int:
    '''ASCII code, *17, modulo 256 for each char'''
    current_value = 0
    for char in list(string):
        current_value += ord(char)
        current_value *= 17
        current_value = current_value % 256
    return current_value


def solve_part_one(strings: list[str]):
    '''determine sum of hashed values for the initialization sequence'''
    with Pool() as pool:
        hashed_values = pool.map(hash_string, strings)
    return sum(hashed_values)


def solve_part_two(strings: list[str]):
    '''
    256 boxes with several lens slots
    fill boxes with label and focal_length accordingly
    generate focus power accordingly
    example: rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
    result: 145
    '''
    boxes = {}
    for string in strings:
        if '=' in string:
            label = string.split('=')[0]
            focal_length = string.split('=')[1]
            box_number = hash_string(label)
            if box_number not in boxes:
                boxes.update({box_number: []})
                boxes[box_number].append(label + focal_length)
                continue
            found = False
            for index, lens in enumerate(boxes[box_number]):
                if label in lens:
                    boxes[box_number][index] = label + focal_length
                    found = True
                    break
            if not found:
                boxes[box_number].append(label + focal_length)
        if '-' in string:
            label = string.split('-')[0]
            box_number = hash_string(label)
            if box_number not in boxes:
                continue
            for index, lens in enumerate(boxes[box_number]):
                if label in lens:
                    del boxes[box_number][index]
                    break
    focus_powers = []
    for box, lenses in boxes.items():
        for index, lens in enumerate(lenses):
            focus_power = 1 + box
            focus_power *= (index + 1)
            focus_power *= int(lens[-1])
            focus_powers.append(focus_power)
    return sum(focus_powers)


if __name__ == '__main__':
    print('Day 15:')
    day15_input = join(dirname(dirname(__file__)), 'input', 'day15.input')
    day15_strings = read_input(day15_input)
    print(f'part one: {solve_part_one(day15_strings)}')
    day15_strings = read_input(day15_input)
    print(f'part two: {solve_part_two(day15_strings)}')
