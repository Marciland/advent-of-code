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

# loop while not at ZZZ, if node[0] in network == 'ZZZ'
# count steps
# if 'L' go to node[0] in network == current_node[1]
# if 'R' go to node[0] in network == current_node[2]


'''
Starting with AAA, you need to look up the next element based on the next left/right instruction in your input
If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL...
Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
'''
list_of_instructions, list_of_nodes = read_input()
# part one
print('')
