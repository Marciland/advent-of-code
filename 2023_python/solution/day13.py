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
from os.path import dirname, join


def read_input(file_path: str) -> list[list[list[str]]]:
    '''formats the day13.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
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
    '''finds the reflection'''
    joined_rows = []
    for row in pattern:
        joined_rows.append(''.join(row))
    rows_above = find_reflection(joined_rows)
    if rows_above:
        return 100*rows_above
    joined_cols = []
    for index in range(0, len(pattern[0]), 1):
        col = ''
        for row in pattern:
            col += row[index]
        joined_cols.append(col)
    columns_left = find_reflection(joined_cols)
    if columns_left:
        return columns_left
    return None


def solve_part_one(patterns):
    '''solve part one, find reflection for each pattern'''
    with multiprocessing.Pool() as pool:
        return sum(pool.map(find_reflections, patterns))


def find_reflection(pattern, start_index=0):
    '''need perfect reflection'''
    for index in range(start_index, len(pattern) - 1, 1):
        if reflects(pattern, index, index+1):
            return index + 1
    return None


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


def solve_part_two(patterns):
    '''solve part two, smudge on mirrors'''
    with multiprocessing.Pool() as pool:
        return sum(pool.map(find_reflections_smudge, patterns))


def find_reflections_smudge(pattern: list[list[str]]):
    '''
    finds the reflection with smudge "somewhere"
    smudge: exactly one . or # should be the opposite type.
    '''
    joined_rows = []
    joined_cols = []
    for row in pattern:
        joined_rows.append(''.join(row))
    for index in range(0, len(pattern[0]), 1):
        col = ''
        for row in pattern:
            col += row[index]
        joined_cols.append(col)
    initial_rows = find_reflection(joined_rows)
    initial_cols = find_reflection(joined_cols)
    for y_index in range(0, len(pattern), 1):
        for x_index in range(0, len(pattern[0]), 1):
            pattern[y_index][x_index] = '.' if pattern[y_index][x_index] == '#' else '#'
            joined_rows = []
            joined_cols = []
            for row in pattern:
                joined_rows.append(''.join(row))
            for index in range(0, len(pattern[0]), 1):
                col = ''
                for row in pattern:
                    col += row[index]
                joined_cols.append(col)
            rows_above = find_reflection(joined_rows)
            if rows_above:
                if rows_above == initial_rows:
                    temp_rows_above = find_reflection(joined_rows,
                                                      start_index=rows_above)
                    if temp_rows_above:
                        rows_above = temp_rows_above
            columns_left = find_reflection(joined_cols)
            if columns_left:
                if columns_left == initial_cols:
                    temp_columns_left = find_reflection(joined_cols,
                                                        start_index=columns_left)
                    if temp_columns_left:
                        columns_left = temp_columns_left
            pattern[y_index][x_index] = '.' if pattern[y_index][x_index] == '#' else '#'
            if rows_above is None and columns_left is None:
                continue
            if rows_above is None:
                if columns_left == initial_cols:
                    continue
            if columns_left is None:
                if rows_above == initial_rows:
                    continue
            if initial_rows == rows_above:
                return columns_left
            if initial_cols == columns_left:
                return 100 * rows_above
    return None


if __name__ == '__main__':
    print('Day 13:')
    day13_input = join(dirname(dirname(__file__)), 'input', 'day13.input')
    day13_patterns = read_input(day13_input)
    print(f'part one: {solve_part_one(day13_patterns)}')
    day13_patterns = read_input(day13_input)
    print(f'part two: {solve_part_two(day13_patterns)}')
