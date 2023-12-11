'''https://adventofcode.com/2023/day/5'''
from os.path import dirname, join


def read_input(file_path: str) -> tuple[list[int], list[list[dict]]]:
    '''formats the day5.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    seeds = file_content[0]
    seeds = [int(number.strip()) for number in seeds.split(' ')
             if number.strip().isnumeric()]
    # cut out seeds and emptylines then strip
    file_content = [line.strip() for line in file_content if line.strip()
                    and not 'seeds:' in line.strip()]
    map_delimiter = []
    for index in range(0, len(file_content), 1):
        if ':' in file_content[index]:
            # start and stop at line contains ':'
            map_delimiter.append(index)
    # add stop at end of file
    map_delimiter.append(len(file_content))
    basic_maps = []
    # for each start, stop couple
    for index in range(0, len(map_delimiter)-1, 1):
        # index = start, index+1 = stop
        basic_map = []
        for i in range(map_delimiter[index]+1, map_delimiter[index+1]):
            splitted_content = file_content[i].split(' ')
            basic_map.append({'dst': int(splitted_content[0]),
                              'src': int(splitted_content[1]),
                              'range_len': int(splitted_content[2])})
            # basic_map.append({'dst': '2797638787', 'src': '1764015146', 'len': '26675178'})
        basic_maps.append(basic_map)
    return seeds, basic_maps


def get_lowest_location(seeds: list[str], maps: list[list[dict]]) -> int:
    '''
    - convert seeds to locaton using all maps
    - return lowest location
    - would not work with negative values in range_len
    '''
    location_numbers = []
    for seed in seeds:
        # start at seed
        current_value = seed
        for _map in maps:
            # reset next
            next_value = None
            for entry in _map:
                dst, src, range_len = entry.items()
                # update next on match
                if src[1] <= current_value <= src[1]+range_len[1]-1:
                    diff = dst[1] - src[1]
                    next_value = current_value + diff
                    break
            # keep value of not matched
            current_value = next_value or current_value
        # last current_value is the location number
        location_numbers.append(current_value)
    lowest_location = -1
    for location_number in location_numbers:
        if lowest_location == -1:
            lowest_location = location_number
        if location_number < lowest_location:
            lowest_location = location_number
    return lowest_location


def read_input_two(file_path: str) -> tuple[list[int], list[list[tuple[int, int, int]]]]:
    '''formats the day5.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    seeds = file_content[0]
    seeds = [int(number.strip()) for number in seeds.split(' ')
             if number.strip().isnumeric()]
    # cut out seeds and emptylines then strip
    file_content = [line.strip() for line in file_content if line.strip()
                    and not 'seeds:' in line.strip()]
    map_delimiter = []
    for index in range(0, len(file_content), 1):
        if ':' in file_content[index]:
            # start and stop at line contains ':'
            map_delimiter.append(index)
    # add stop at end of file
    map_delimiter.append(len(file_content))
    basic_maps = []
    # for each start, stop couple
    for index in range(0, len(map_delimiter)-1, 1):
        # index = start, index+1 = stop
        basic_map = []
        for i in range(map_delimiter[index]+1, map_delimiter[index+1]):
            splitted_content = file_content[i].split(' ')
            basic_map.append((int(splitted_content[0]),
                              int(splitted_content[1]),
                              int(splitted_content[2])))
        basic_maps.append(basic_map)
    return seeds, basic_maps


def get_lowest_location_two(seeds: tuple[list[int]], maps: list[list[tuple[int, int, int]]]):
    '''reversed?'''
    maps.reverse()
    locations = maps[0].copy()
    locations.sort()
    maps.remove(maps[0])
    for entry in locations:
        lowest_location = entry[0]
        for location in range(entry[1], entry[1] + entry[2] - 1, 1):
            done = False
            current_value = location
            for mapping in maps:
                next_value = None
                for entry in mapping:
                    if entry[0] <= current_value <= entry[0]+entry[2]-1:
                        diff = entry[0] - entry[1]
                        next_value = current_value - diff
                        break
                current_value = next_value or current_value
            for i in range(0, len(seeds)-1, 2):
                if seeds[i] <= current_value <= seeds[i] + seeds[i+1]-1:
                    done = True
            if done:
                break
            lowest_location += 1
        if done:
            break
    return lowest_location


def solve_part_one(seeds_list: list[int], map_list: list[list[dict]]):
    return get_lowest_location(seeds_list, map_list)


def solve_part_two(seeds_list: list[int], map_list: list[list[tuple[int, int, int]]]):
    return get_lowest_location_two(seeds_list, map_list)


if __name__ == '__main__':
    print('Day 5:')
    day5_input = join(dirname(dirname(__file__)), 'input', 'day5.input')
    day5_seeds, day5_basic_maps = read_input(day5_input)
    print(f'part one: {solve_part_one(day5_seeds, day5_basic_maps)}')
    day5_seeds_list, day5_map_list = read_input_two(day5_input)
    print(f'part two: {solve_part_two(day5_seeds_list, day5_map_list)}')
