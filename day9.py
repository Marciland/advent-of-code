'''
https://adventofcode.com/2023/day/9

Oasis And Sand Instability Sensor
Each line in the report contains the history of a single value.
prediction of the next value in each history
difference at each step
Since these values aren't all zero, repeat the process
append to each list:
    result = value_before + value_below
sum the last entry of each list
'''
import os

from helpers import get_sum

day9_input = os.path.join(os.getcwd(), 'day9.txt')


def read_input() -> list[list[int]]:
    '''formats the day9.txt'''
    return []

# for list in input:
# create list to keep difference between each entry
# continue until all entries are 0
#
# reverse newly created lists
# for list in new lists:
# predict new last entry : result = value_before + value_below (value above if reversed)
# based on the last value of the last list -> predict new value for input list in list, append to new result list
# sum result list


if __name__ == '__main__':
    # part one
    print(get_sum(read_input()))
    # expect 114 for the test input
