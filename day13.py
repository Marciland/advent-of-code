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
    joined = []
    for row in pattern:
        joined.append(''.join(row))
    horizontal_matches, rows_above = get_highest_match(joined)
    joined = []
    for index in range(0, len(pattern[0]), 1):
        col = ''
        for row in pattern:
            col += row[index]
        joined.append(col)
    vertical_matches, columns_left = get_highest_match(joined)
    if horizontal_matches > vertical_matches:
        return 100*rows_above
    return columns_left


def solve_part_one():
    '''solve part one, find reflection for each pattern'''
    patterns = read_input()
    with multiprocessing.Pool() as pool:
        return sum(pool.map(find_reflections, patterns))


def get_highest_match(pattern, index=0, step=0, matches=0, highest=0, high_index=0):
    '''returns highest match count and index (amount of rows above or columns left!)'''
    if index == len(pattern) - 1:
        return highest, high_index+1
    if index+step != len(pattern)-1 and index-step > 0:
        if pattern[index-step] == pattern[index+step+1]:
            return get_highest_match(pattern, index, step+1, matches+1, highest, high_index)
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
    assert one_result > 32271
