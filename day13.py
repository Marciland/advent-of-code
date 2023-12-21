'''
https://adventofcode.com/2023/day/13

ash (.) and rocks (#)
find a perfect reflection across either:
- a horizontal line between two rows
- or across a vertical line between two columns

add up the number of columns to the left of each vertical line of reflection
add 100 multiplied by the number of rows above each horizontal line of reflection.

Find the line of reflection in each of the patterns in your notes.
What number do you get after summarizing all of your notes?

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

result: 405 (5 (to the left in first) + 100 * 4(rows above in second))
'''
import multiprocessing
import os
from time import perf_counter

day13_input = os.path.join(os.getcwd(), 'day13.txt')


def read_input() -> list[list[list[str]]]:
    '''formats the day13.txt'''
    with open(day13_input, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    delimiter = []
    delimiter.append(-1)
    for i, line in enumerate(file_content):
        if not line.strip():
            delimiter.append(i)
    delimiter.append(len(file_content))
    patterns = []
    for index in range(0, len(delimiter)-1, 1):
        pattern_rows = []
        for i in range(delimiter[index]+1, delimiter[index+1]):
            pattern_cols = []
            for symbol in file_content[i].strip():
                pattern_cols.append(symbol)
            pattern_rows.append(pattern_cols)
        patterns.append(pattern_rows)
    return patterns


def find_reflections(pattern: list[list[str]]):
    '''finds the best reflection match'''
    joined_rows = []
    for row in pattern:
        joined_rows.append(''.join(row))
    rows_above = find_reflection(joined_rows)
    joined_cols = []
    for index in range(0, len(pattern[0]), 1):
        col = ''
        for row in pattern:
            col += row[index]
        joined_cols.append(col)
    columns_left = find_reflection(joined_cols)
    if rows_above:
        return 100*rows_above
    return columns_left


def solve_part_one():
    '''solve part one, find reflection for each pattern'''
    patterns = read_input()
    with multiprocessing.Pool() as pool:
        return sum(pool.map(find_reflections, patterns))


def find_reflection(pattern):
    '''need perfect reflection'''
    for index in range(0, len(pattern) - 1, 1):
        if reflects(pattern, index, index+1):
            return index + 1


def reflects(pattern, left, right):
    '''
    if leaving vision -> true
    if not reflecting false
    '''
    if left < 0:
        return True
    if right > len(pattern)-1:
        return True
    if pattern[left] == pattern[right]:
        return reflects(pattern, left-1, right+1)
    return False


def get_highest_match(pattern, index=0, step=0, matches=0, highest=0, high_index=0):
    '''returns highest match count and index (amount of rows above or columns left!)'''
    if index == len(pattern) - 1:
        return highest, high_index+1
    if index+step != len(pattern)-1 and index-step > 0:
        if pattern[index-step] == pattern[index+step+1]:
            return get_highest_match(pattern, index, step+1, matches+1, highest, high_index)
    else:
        if high_index != 0:
            return highest, high_index+1
    if matches > highest:
        highest = matches
        high_index = index
    matches = 0
    step = 0
    return get_highest_match(pattern, index+1, step, matches, highest, high_index)


if __name__ == '__main__':
    start_time = perf_counter()
    one_result = solve_part_one()
    one_time = perf_counter() - start_time
    print('Result:', one_result)
    print('Time:', one_time)
