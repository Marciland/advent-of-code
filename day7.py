'''
https://adventofcode.com/2023/day/7

play camel cards like poker
'''
import os

from helpers import get_sum

day7_input = os.path.join(os.getcwd(), 'day7.txt')


def read_input() -> list[tuple[str, int]]:
    '''formats the day7.txt'''
    with open(day7_input, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    cards = []
    bids = []
    for line in file_content:
        cards.append(line.split(' ')[0].strip())
        bids.append(int(line.split(' ')[1].strip()))
    hands = []
    for index in range(0, len(cards), 1):
        hands.append((cards[index], bids[index]))
    return hands


def set_hands_power(hands: list[tuple[str, int]]) -> list[tuple[str, int, int]]:
    '''
    for hand in hands
    generate a power:
    A > K > Q > J > T > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2
    fünfling > vierling > full house > drilling > doppelpaar > pärchen > high card
    '''


def order_hands(hands: list[tuple[str, int, int]]) -> list[int]:
    '''
    sort by comparing power
    if two hands are the same "power" -> compare the first card -> compare the second ... etc
    A > K > Q > J > T > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2

    every hand has a bid
    the weakest hand has rank 1
    the strongest hand has rank n
    multiply bid by n and create a sum of all hands

    1.  sort list
    1.1 compare hands, create new list
    2.  collect bid * rank
    3.  create sum
    '''


# part one
print(get_sum(order_hands(set_hands_power(read_input()))))
