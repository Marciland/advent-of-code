'''https://adventofcode.com/2023/day/6'''
import os
from time import perf_counter

from helpers import get_product


def read_input(file_path: str) -> list[tuple[int, int]]:
    '''formats the day6.txt'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    times = [int(time.strip()) for time in file_content[0].split(' ')
             if time.strip().isnumeric()]
    distances = [int(distance.strip()) for distance in file_content[1].split(' ')
                 if distance.strip().isnumeric()]
    races = []
    for index in range(0, len(times), 1):
        races.append((times[index], distances[index]))
    return races


def read_input_two(file_path: str) -> list[tuple[int, int]]:
    '''formats the day6.txt'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    times = [time.strip() for time in file_content[0].split(' ')
             if time.strip().isnumeric()]
    distances = [distance.strip() for distance in file_content[1].split(' ')
                 if distance.strip().isnumeric()]
    time = int(''.join(times))
    distance = int(''.join(distances))
    return [(time, distance)]


def get_possibilities(races: list[tuple[int, int]]) -> list[int]:
    '''
    speed = time button pressed
    distance reached = (race[time] - speed) * speed
    win if distance reached > race[distance]
    if win increase possible counter
    for each race append possible counter

    for time in race[time] check
    do not press the button the entire duration
    do not not press the button
    '''
    possibilities = []
    for race in races:
        win_counter = 0
        # do not include 0 and len(race[0])!
        for pressed in range(1, race[0], 1):
            # pressed = time button is pressed -> speed
            distance = (race[0] - pressed) * pressed
            if race[1] < distance:
                win_counter += 1
        possibilities.append(win_counter)
    return possibilities


def solve_part_one(races: list[tuple[int, int]]):
    print(get_product(get_possibilities(races)))


def solve_part_two(races: list[tuple[int, int]]):
    print(get_product(get_possibilities(races)))


def solve():
    print('Day 6:')
    day6_input = os.path.join(os.getcwd(), 'input', 'day6.txt')
    print('part one: ', end='')
    start_time = perf_counter()
    races = read_input(day6_input)
    solve_part_one(races)
    print('solved in:', perf_counter() - start_time)
    print('part two: ', end='')
    start_time = perf_counter()
    races = read_input_two(day6_input)
    solve_part_two(races)
    print('solved in:', perf_counter() - start_time)
