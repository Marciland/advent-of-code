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


def navigate_network_two(instructions, nodes) -> int:
    '''
    start at all nodes with locations ending in A
    navigate with the instructions through nodes simultaneously
    stop when all nodes reached a location ending with Z
    return steps taken
    '''
    starting_locations = []
    for node in nodes:
        if is_start_node(node[0]):
            starting_locations.append(node[0])
    temp_list = starting_locations.copy()
    hits = 0
    steps = 0
    while True:
        for instruction in instructions:
            # return steps if all nodes hit the end at the same time (hits = amount of nodes)
            if hits == len(starting_locations):
                return steps
            # do not increase hits, instead set to hits each instruction
            current_hits = 0
            for location in starting_locations:
                temp_list.remove(location)
                next_location = find_location(location, nodes, instruction)
                if is_end_node(next_location):
                    current_hits += 1
                temp_list.append(next_location)
            hits = current_hits
            starting_locations = temp_list.copy()
            # increase each instruction anyways
            steps += 1


list_of_instructions, list_of_nodes = read_input()
# part one
print(navigate_network(list_of_instructions, list_of_nodes))
# part two
print(navigate_network_two(list_of_instructions, list_of_nodes))
