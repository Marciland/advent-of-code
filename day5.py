'''https://adventofcode.com/2023/day/5'''
import os

day5_input = os.path.join(os.getcwd(), 'day5.txt')


def read_input() -> tuple[list[str], list[list[dict]]]:
    '''formats the day5.txt'''
    with open(day5_input, 'r', encoding='utf-8') as file_handle:
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


def generate_conversion_table(basic_map: list[dict]) -> list[tuple[int, int]]:
    '''
    BRUTEFORCE!!!!
    This is what i get from read_input:
    destination range start, source range start, range length
    dst,  src,    range_len
    50    98      2
    52    50      48

    This is what i want to return:
    from  to
    X     Y
    '''
    conversion_table = []
    for entry in basic_map:
        dst, src, range_len = entry.items()
        for index in range(range_len[1]):
            conversion_table.append((src[1]+index, dst[1]+index))
    # return list of (from, to)
    return conversion_table


def get_lowest_location_brute(seeds: list[str], maps: list[list[dict]]) -> int:
    '''
    BRUTEFORCE!!!!
    - generate table for each category
    - convert seeds to locaton using all tables
    - return lowest location
    '''
    conversion_tables = []
    for basic_map in maps:
        # create a table to read from to conversions
        conversion_tables.append(generate_conversion_table(basic_map))
    location_numbers = []
    for seed in seeds:
        # start at seed
        current_value = seed
        for conversion_table in conversion_tables:
            # reset next
            next_value = None
            for entry in conversion_table:
                # update next on match
                if current_value == entry[0]:
                    next_value = entry[1]
            # keep value if not matched
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
                if current_value >= src[1] and current_value <= src[1]+range_len[1]:
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


seed_list, map_list = read_input()
print(get_lowest_location(seed_list, map_list))  # part one
