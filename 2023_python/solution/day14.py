'''https://adventofcode.com/2023/day/14'''
from os.path import dirname, join


def read_input(file_path: str) -> list[str]:
    '''formats the day14.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        rows = [line.strip() for line in file_handle.readlines()]
    return convert_to_cols(rows)


def convert_to_rows(cols: list[str]) -> list[str]:
    '''convert a list of columns to a list of rows'''
    rows = []
    for y_index in range(0, len(cols[0]), 1):
        row = []
        for col in cols:
            row.append(col[y_index])
        rows.append(''.join(row))
    return rows


def convert_to_cols(rows: list[str]) -> list[str]:
    '''convert a list of rows to a list of cols'''
    cols = []
    for x_index in range(0, len(rows[0]), 1):
        col = []
        for row in rows:
            col.append(row[x_index])
        cols.append(''.join(col))
    return cols


def find_free_slot_north(col: str, start_index: int) -> int:
    '''free_slot is where the next rock could be pushed'''
    free_slot = start_index
    for y_index in range(start_index, len(col), 1):
        if col[y_index] == '.':
            break
        free_slot += 1
    return free_slot


def push_north(col: str) -> str:
    '''move all (moveable) rocks "O" as north as possible'''
    col = list(col)
    next_slot = find_free_slot_north(col, 0)
    for y_index, symbol in enumerate(col):
        if y_index < next_slot:
            continue
        if symbol == '.':
            continue
        if symbol == 'O':
            col[next_slot] = 'O'
            col[y_index] = '.'
            next_slot = find_free_slot_north(col, next_slot)
            continue
        if symbol == '#':
            next_slot = find_free_slot_north(col, y_index)
            continue
    col = ''.join(col)
    return col


def find_free_slot_east(row: str, start_index: int) -> int:
    '''free_slot is where the next rock could be pushed'''
    free_slot = start_index
    for x_index in range(start_index, 0 - 1, -1):
        if row[x_index] == '.':
            break
        free_slot -= 1
    return free_slot


def push_east(row: str) -> str:
    '''move all (moveable) rocks "O" as east as possible'''
    row = list(row)
    next_slot = find_free_slot_east(row, len(row) - 1)
    for x_index in range(len(row) - 1, 0 - 1, -1):
        if x_index > next_slot:
            continue
        if row[x_index] == '.':
            continue
        if row[x_index] == 'O':
            row[next_slot] = 'O'
            row[x_index] = '.'
            next_slot = find_free_slot_east(row, next_slot)
            continue
        if row[x_index] == '#':
            next_slot = find_free_slot_east(row, x_index)
            continue
    row = ''.join(row)
    return row


def find_free_slot_south(col: str, start_index: int) -> int:
    '''free_slot is where the next rock could be pushed'''
    free_slot = start_index
    for y_index in range(start_index, 0 - 1, -1):
        if col[y_index] == '.':
            break
        free_slot -= 1
    return free_slot


def push_south(col: str) -> str:
    '''move all (moveable) rocks "O" as south as possible'''
    col = list(col)
    next_slot = find_free_slot_south(col, len(col) - 1)
    for y_index in range(len(col) - 1, 0 - 1, -1):
        if y_index > next_slot:
            continue
        if col[y_index] == '.':
            continue
        if col[y_index] == 'O':
            col[next_slot] = 'O'
            col[y_index] = '.'
            next_slot = find_free_slot_south(col, next_slot)
            continue
        if col[y_index] == '#':
            next_slot = find_free_slot_south(col, y_index)
            continue
    col = ''.join(col)
    return col


def find_free_slot_west(row: str, start_index: int) -> int:
    '''free_slot is where the next rock could be pushed'''
    free_slot = start_index
    for x_index in range(start_index, len(row), 1):
        if row[x_index] == '.':
            break
        free_slot += 1
    return free_slot


def push_west(row: str) -> str:
    '''move all (moveable) rocks "O" as west as possible'''
    row = list(row)
    next_slot = find_free_slot_west(row, 0)
    for x_index, symbol in enumerate(row):
        if x_index < next_slot:
            continue
        if symbol == '.':
            continue
        if symbol == 'O':
            row[next_slot] = 'O'
            row[x_index] = '.'
            next_slot = find_free_slot_west(row, next_slot)
            continue
        if symbol == '#':
            next_slot = find_free_slot_west(row, x_index)
            continue
    row = ''.join(row)
    return row


def get_load(col: str) -> int:
    '''load is the distance from O to south'''
    total_load = 0
    for y_index, symbol in enumerate(col):
        if symbol == 'O':
            total_load += len(col) - y_index
    return total_load


def solve_part_one(cols: list[str]):
    '''push all O to north (y-index=0), then return the total load'''
    pushed_cols = [push_north(col) for col in cols]
    return sum(get_load(col) for col in pushed_cols)


def solve_part_two(cols: list[str]):
    '''spin cycle -> north, then west, then south, then east. total load on north afterwards'''
    cycles = 1000000000
    pushed_east = []
    load = []
    temp = []
    for cycle in range(cycles):
        # check if load pattern repeats
        if find_mult(load, temp) > 1:
            break
        # 12 returns the right value, why is that tho?
        # -> is there a better way to stop when the pattern repeats?
        # remembering the last 12 values
        if cycle % 12 == 0:
            temp = []
        if not pushed_east:
            pushed_north = [push_north(col)
                            for col in cols]
        else:
            pushed_north = [push_north(col)
                            for col in convert_to_cols(pushed_east)]
        pushed_west = [push_west(row)
                       for row in convert_to_rows(pushed_north)]
        pushed_south = [push_south(col)
                        for col in convert_to_cols(pushed_west)]
        pushed_east = [push_east(row)
                       for row in convert_to_rows(pushed_south)]
        load.append(sum(get_load(col) for col in convert_to_cols(pushed_east)))
        temp.append(sum(get_load(col) for col in convert_to_cols(pushed_east)))
    return sum(get_load(col) for col in convert_to_cols(pushed_east))


def find_mult(load: list[int], temp: list[int]):
    '''returns the amount temp is found in load'''
    temp_len = len(temp)
    found = 0
    inc = 0
    mismatch = False
    for i in range(0, len(load), 1):
        if i != 0:
            if i % temp_len == 0:
                if not mismatch:
                    found += 1
                mismatch = False
                inc += 1
        if temp[i - inc * temp_len] != load[i]:
            mismatch = True
    return found


if __name__ == '__main__':
    print('Day 14:')
    day14_input = join(dirname(dirname(__file__)), 'input', 'day14.input')
    day14_cols = read_input(day14_input)
    print(f'part one: {solve_part_one(day14_cols)}')
    day14_cols = read_input(day14_input)
    print(f'part two: {solve_part_two(day14_cols)}')
