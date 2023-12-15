'''
https://adventofcode.com/2023/day/8

navigate L or R on the network
'''
import os

day8_input = os.path.join(os.getcwd(), 'day8.txt')


def read_input() -> tuple[list[str], list[tuple[str, str, str]]]:
    '''formats the day8.txt'''
    with open(day8_input, 'r', encoding='utf-8') as file_handle:
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
        temp = number1
        number1 = number2
        number2 = temp
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
    import multiprocessing
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


if __name__ == '__main__':
    list_of_instructions, list_of_nodes = read_input()
    # part one
    print(navigate_network(list_of_instructions, list_of_nodes))
    # part two
    print(navigate_network_multi(list_of_instructions, list_of_nodes))
