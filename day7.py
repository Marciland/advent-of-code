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
    fünfling > vierling > full house > drilling > doppelpaar > pärchen > high card
        6    >     5    >     4      >    3     >      2     >    1    >    0
    '''
    hands_with_power = []
    for hand in hands:
        counter_list = []
        cards = hand[0]
        for index in range(0, len(cards), 1):
            counter = 0
            current_card = cards[index]
            for card in cards:
                if current_card == card:
                    counter += 1
            counter_list.append(counter)
        if counter_list.count(1) == 5:
            hand = (hand[0], hand[1], 0)
        if counter_list.count(2) == 2 and not counter_list.count(3) == 3:
            hand = (hand[0], hand[1], 1)
        if counter_list.count(2) == 4:
            hand = (hand[0], hand[1], 2)
        if counter_list.count(3) == 3 and not counter_list.count(2) == 2:
            hand = (hand[0], hand[1], 3)
        if counter_list.count(3) == 3 and counter_list.count(2) == 2:
            hand = (hand[0], hand[1], 4)
        if counter_list.count(4) == 4:
            hand = (hand[0], hand[1], 5)
        if counter_list.count(5) == 5:
            hand = (hand[0], hand[1], 6)
        hands_with_power.append(hand)
    # lowest power is at lowest index now!
    hands_with_power = sorted(hands_with_power, key=lambda hand: hand[2])
    return hands_with_power


def get_card_value(card):
    '''A > K > Q > J > T > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2'''
    match(card):
        case 'T':
            value = 10
        case 'J':
            value = 11
        case 'Q':
            value = 12
        case 'K':
            value = 13
        case 'A':
            value = 14
        case _:
            value = int(card)
    return value


def card_is_better(card, sorted_card) -> bool:
    '''True if the card is better than the card from the sorted hand'''
    return get_card_value(card) > get_card_value(sorted_card)


def hand_is_better(hand, sorted_hand) -> bool:
    '''
    True if hand is better than sorted hand.
    compare the first card -> compare the second ... etc
    '''
    for index in range(0, len(hand), 1):
        # compare next if they are the same
        if hand[0][index] == sorted_hand[0][index]:
            continue
        # if a better card in hand is found, just return True
        if card_is_better(hand[0][index], sorted_hand[0][index]):
            break
        return False
    return True


def get_list_of_powers(hands: list[tuple[str, int, int]]):
    '''create lists for each power! last card needs to append last list'''
    list_of_powers = []
    new_list = []
    current_power = -1
    for hand in hands:
        if current_power != hand[2]:
            if new_list:
                list_of_powers.append(new_list)
            new_list = []
            current_power = hand[2]
        new_list.append(hand)
        if hand == hands[-1]:
            list_of_powers.append(new_list)
    return list_of_powers


def order_power(power):
    '''for a type/power sort all hands'''
    sorted_hands = []
    # sort hands into sorted_power, weakest at 0, highest at -1
    while True:
        if len(sorted_hands) == len(power):
            break
        for hand in power:
            inserted = False
            # do not add hands twice
            if hand in sorted_hands:
                continue
            # the first hand should just be appended
            if not sorted_hands:
                sorted_hands.append(hand)
                continue
            for sorted_hand in sorted_hands:
                if sorted_hand == hand:
                    continue
                # compare first card, then second, etc
                if hand_is_better(hand, sorted_hand):
                    # expect all hands to be unique
                    index = sorted_hands.index(sorted_hand)
                    # +1 because better has higher index
                    sorted_hands.insert(index+1, hand)
                    inserted = True
                    # only works if a worse card is found in sorted_hand
                    break
            if not inserted:
                # insert at first index if hand is the worst
                sorted_hands.insert(0, hand)
    return sorted_hands

# TODO! do not insert after a hand that is worse than the hand we want to insert
# keep the index and find the highest index of a worse hand
# insert as high as possible
# instead of if not inserted, use if index is None to insert the worst hand

def get_ranks(hands: list[tuple[str, int, int]]) -> list[int]:
    '''
    sort by comparing power
    if two hands are the same "power" -> compare the first card -> compare the second ... etc
    A > K > Q > J > T > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2
    '''
    list_of_powers = get_list_of_powers(hands)
    # sort each power in itself!
    sorted_hands = []
    # power contains all hands with the same power
    for power in list_of_powers:
        sorted_hands.append(order_power(power))
    # this only works if sorted_hands only contains lists!!
    sorted_hands = [hand for hands in sorted_hands for hand in hands]
    bids_with_ranks = []
    # collect bid * rank for each hand
    for rank in range(1, len(sorted_hands)+1, 1):
        # rank 1 is index 0! thus -1
        bids_with_ranks.append(sorted_hands[rank-1][1] * rank)
    return bids_with_ranks


# part one
print(get_sum(get_ranks(set_hands_power(read_input()))))
