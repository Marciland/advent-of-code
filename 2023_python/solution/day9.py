'''
https://adventofcode.com/2023/day/9

Oasis And Sand Instability Sensor
Each line in the report contains the history of a single value.
prediction of the next value in each history
difference at each step
Since these values aren't all zero, repeat the process
append to each list:
    result = value_before + value_below
sum the last entry of each list
'''
from os.path import dirname, join


def read_input(file_path: str) -> list[list[int]]:
    '''formats the day9.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    histories = []
    for line in file_content:
        history = []
        for number in line.split(' '):
            history.append(int(number.strip()))
        histories.append(history)
    return histories


def only_zero(lis: list) -> bool:
    '''if all entries in lis are 0 return True'''
    return lis.count(0) == len(lis)


def generate_differences(history: list[int]) -> list[list[int]]:
    '''
    create a pyramid (list of lists) that contains the differences
    0   3   6   9  12  15
      3   3   3   3   3
        0   0   0   0
    '''
    pyramid = []
    pyramid.append(history)
    while True:
        # if all values at the last index are 0
        if only_zero(pyramid[-1]):
            break
        differences = []
        for index in range(0, len(pyramid[-1])-1, 1):
            differences.append(pyramid[-1][index+1] - pyramid[-1][index])
        pyramid.append(differences)
    return pyramid


def predict_next(history: list[int]) -> int:
    '''predict new last entry : result = value_before + value_below (value above if reversed)'''
    differences = generate_differences(history)
    differences.reverse()
    for index in range(1, len(differences)-1, 1):
        x = differences[index][-1]
        y = differences[index+1][-1]
        differences[index+1].append(x+y)
    # based on the last value of the last list
    return differences[-1][-1]


def predict_previous(history: list[int]) -> int:
    '''predict new first entry : result = value_below - value above'''
    differences = generate_differences(history)
    differences.reverse()
    for index in range(1, len(differences)-1, 1):
        x = differences[index][0]
        y = differences[index+1][0]
        differences[index+1].insert(0, y-x)
    # based on the first value of the last list
    return differences[-1][0]


def solve_part_one(histories: list[list[int]]):
    next_values = []
    for list_of_numbers in histories:
        next_values.append(predict_next(list_of_numbers))
    return sum(next_values)


def solve_part_two(histories: list[list[int]]):
    previous_values = []
    for list_of_numbers in histories:
        previous_values.append(predict_previous(list_of_numbers))
    return sum(previous_values)


if __name__ == '__main__':
    print('Day 9:')
    day9_input = join(dirname(dirname(__file__)), 'input', 'day9.input')
    day9_histories = read_input(day9_input)
    print(f'part one: {solve_part_one(day9_histories)}')
    day9_histories = read_input(day9_input)
    print(f'part two: {solve_part_two(day9_histories)}')
