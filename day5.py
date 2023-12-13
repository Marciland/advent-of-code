'''https://adventofcode.com/2023/day/5'''
import os

day5_input = os.path.join(os.getcwd(), 'day5.txt')


def read_input():
    '''formats the day5.txt'''

# destination range start, source range start, range length
# 50 98 2
# 52 50 48

# seed 98 maps on soil 50
# seed 99 maps on soil 51
# seeds 50-97 map on soils 52-99
# if not in map: destination = source
# seed 10 maps on soil 10

'''
seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
'''

# source category to destination category:
# seed to soil
# soil-to-fertilizer
# fertilizer-to-water
# water-to-light
# light-to-temperature
# temperature-to-humidity
# humidity-to-location

# get all location numbers for seeds
# get the lowest location number

print()  # part one
