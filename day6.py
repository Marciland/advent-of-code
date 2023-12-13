'''https://adventofcode.com/2023/day/6'''
import os

from helpers import get_product

day6_input = os.path.join(os.getcwd(), 'day6.txt')


def read_input() -> list[tuple[int, int]]:
    '''formats the day6.txt'''
    with open(day6_input, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    times = [int(time.strip()) for time in file_content[0].split(' ')
             if time.strip().isnumeric()]
    distances = [int(distance.strip()) for distance in file_content[1].split(' ')
                 if distance.strip().isnumeric()]
    races = []
    for index in range(0, len(times), 1):
        races.append((times[index], distances[index]))
    return races


def read_input_two() -> list[tuple[int, int]]:
    '''formats the day6.txt'''
    with open(day6_input, 'r', encoding='utf-8') as file_handle:
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


# part one
print(get_product(get_possibilities(read_input())))
# part two
print(get_product(get_possibilities(read_input_two())))
