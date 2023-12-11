'''
https://adventofcode.com/2023/day/8

navigate L or R on the network
'''
import multiprocessing
from os.path import dirname, join


def read_input(file_path: str) -> tuple[list[str], list[tuple[str, str, str]]]:
    '''formats the day8.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    instructions = list(file_content[0].strip())
    file_content = [line.strip() for line in file_content[1:] if line.strip()]
    network = []
    for line in file_content:
        location = line.split('=')[0].strip()
        left_instruction = line.split('(')[1].split(',')[0].strip()
        right_instruction = line.split(',')[1].strip().replace(')', '')
        network.append((location, left_instruction, right_instruction))
    return instructions, network


def navigate_network(instructions, nodes) -> int:
    '''
    start at AAA
    navigate with the instructions through nodes
    stop when ZZZ is reached
    return steps taken
    '''
    start = 'AAA'
    end = 'ZZZ'
    steps = 0
    current_location = start
    while True:
        for instruction in instructions:
            if current_location == end:
                return steps
            for node in nodes:
                if node[0] == current_location:
                    current_location = node[1] if instruction == 'L' else node[2]
                    steps += 1
                    break


def is_start_node(node: str) -> bool:
    return node[-1] == 'A'


def is_end_node(node: str) -> bool:
    return node[-1] == 'Z'


def find_location(location: str, nodes: list, instruction: str):
    for node in nodes:
        if node[0] == location:
            return node[1] if instruction == 'L' else node[2]


def calc_steps(location, instructions, nodes, steps: list):
    '''get range from start to end'''
    step = 0
    while True:
        for instruction in instructions:
            location = find_location(location, nodes, instruction)
            step += 1
            if is_end_node(location):
                steps.append(step)
                return


def calc_kgv(number1, number2):
    a = number1
    b = number2
    if number1 < number2:
        number1, number2 = number2, number1
    rest = number1 % number2
    while rest != 0:
        number1 = number2
        number2 = rest
        rest = number1 % number2
    return a*b//number2


def navigate_network_multi(instructions, nodes):
    '''
    pregenerate a list of steps to an end node for each starting location
    find the smallest match for all starting locations
    '''
    starting_locations = []
    for node in nodes:
        if is_start_node(node[0]):
            starting_locations.append(node[0])
    steps = multiprocessing.Manager().list()
    processes = []
    for location in starting_locations:
        process = multiprocessing.Process(
            target=calc_steps, args=(location, instructions, nodes, steps))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    return calc_kgv(calc_kgv(steps[0],
                             calc_kgv(steps[1],
                                      steps[2])),
                    calc_kgv(steps[3],
                             calc_kgv(steps[4],
                                      steps[5])))


def solve_part_one(list_of_instructions: list[str], list_of_nodes: list[tuple[str, str, str]]):
    return navigate_network(list_of_instructions, list_of_nodes)


def solve_part_two(list_of_instructions: list[str], list_of_nodes: list[tuple[str, str, str]]):
    return navigate_network_multi(list_of_instructions, list_of_nodes)


if __name__ == '__main__':
    print('Day 8:')
    day8_input = join(dirname(dirname(__file__)), 'input', 'day8.input')
    day8_list_of_instructions, day8_list_of_nodes = read_input(day8_input)
    print(
        f'part one: {solve_part_one(day8_list_of_instructions, day8_list_of_nodes)}')
    day8_list_of_instructions, day8_list_of_nodes = read_input(day8_input)
    print(
        f'part two: {solve_part_two(day8_list_of_instructions, day8_list_of_nodes)}')
