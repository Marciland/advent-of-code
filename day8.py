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


list_of_instructions, list_of_nodes = read_input()
# part one
print(navigate_network(list_of_instructions, list_of_nodes))
