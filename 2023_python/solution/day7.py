'''
https://adventofcode.com/2023/day/7

play camel cards like poker
'''
from os.path import dirname, join


def read_input(file_path: str) -> list[tuple[str, int]]:
    '''formats the day7.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
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


def swap_list_entry(list_pointer: list, entry, new_value):
    '''change the power of a list entry'''
    list_pointer.remove(entry)
    entry = (entry[0], entry[1], new_value)
    list_pointer.append(entry)


def set_hands_power_two(hands: list[tuple[str, int]]) -> list[tuple[str, int, int]]:
    '''
    fünfling > vierling > full house > drilling > doppelpaar > pärchen > high card
        6    >     5    >     4      >    3     >      2     >    1    >    0
    J will count as any needed
    '''
    hands_with_power = set_hands_power(hands)
    temp = hands_with_power.copy()
    for hand in temp:
        amount_of_j = hand[0].count('J')
        # no joker -> nothing changes
        if amount_of_j == 0:
            continue
        if amount_of_j == 1:
            match(hand[2]):
                case 0:
                    # high card + j = pärchen
                    swap_list_entry(hands_with_power, hand, 1)
                case 1:
                    # pärchen + j = drilling
                    swap_list_entry(hands_with_power, hand, 3)
                case 2:
                    # doppelpaar + j = full house
                    swap_list_entry(hands_with_power, hand, 4)
                case 3:
                    # drilling + j = vierling
                    swap_list_entry(hands_with_power, hand, 5)
                case 5:
                    # vierling + j = fünfling
                    swap_list_entry(hands_with_power, hand, 6)
        if amount_of_j == 2:
            match(hand[2]):
                case 1:
                    # pärchen + 2J = drilling
                    swap_list_entry(hands_with_power, hand, 3)
                case 2:
                    # doppelpaar + 2J = vierling
                    swap_list_entry(hands_with_power, hand, 5)
                case 3:
                    # drilling + 2J = fünfling. amount_of_j != 3
                    swap_list_entry(hands_with_power, hand, 6)
                case 4:
                    # full house + 2J = fünfling
                    swap_list_entry(hands_with_power, hand, 6)
        if amount_of_j == 3:
            match(hand[2]):
                case 3:
                    # drilling + 3J = vierling. amount_of_j + 1 else full house
                    swap_list_entry(hands_with_power, hand, 5)
                case 4:
                    # full house + 3J = fünfling
                    swap_list_entry(hands_with_power, hand, 6)
        if amount_of_j == 4:
            match(hand[2]):
                case 5:
                    # vierling + 4J = fünfling
                    swap_list_entry(hands_with_power, hand, 6)
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


def get_card_value_two(card):
    '''A > K > Q > T > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2 > J'''
    match(card):
        case 'T':
            value = 10
        case 'J':
            value = 1
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


def card_is_better_two(card, sorted_card) -> bool:
    '''True if the card is better than the card from the sorted hand'''
    return get_card_value_two(card) > get_card_value_two(sorted_card)


def hand_is_better(hand, sorted_hand) -> bool:
    '''
    True if hand is better than sorted hand.
    compare the first card -> compare the second ... etc
    '''
    for index in range(0, len(hand[0]), 1):
        # compare next if they are the same
        if hand[0][index] == sorted_hand[0][index]:
            continue
        # if a better card in hand is found, just return True
        if card_is_better(hand[0][index], sorted_hand[0][index]):
            break
        return False
    return True


def hand_is_better_two(hand, sorted_hand) -> bool:
    '''
    True if hand is better than sorted hand.
    compare the first card -> compare the second ... etc
    '''
    for index in range(0, len(hand[0]), 1):
        # compare next if they are the same
        if hand[0][index] == sorted_hand[0][index]:
            continue
        # if a better card in hand is found, just return True
        if card_is_better_two(hand[0][index], sorted_hand[0][index]):
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
            # do not add hands twice
            if hand in sorted_hands:
                continue
            # the first hand should just be appended
            if not sorted_hands:
                sorted_hands.append(hand)
                continue
            index = None
            for sorted_hand in sorted_hands:
                # expect all hands to be unique
                if sorted_hand == hand:
                    continue
                # compare first card, then second, etc
                if hand_is_better(hand, sorted_hand):
                    new_index = sorted_hands.index(sorted_hand)
                    if not index:
                        index = new_index
                        continue
                    if new_index > index:
                        index = new_index
            if index is None:
                # insert at first index if hand is the worst
                sorted_hands.insert(0, hand)
            else:
                # +1 because better has higher index
                sorted_hands.insert(index+1, hand)
    return sorted_hands


def order_power_two(power):
    '''for a type/power sort all hands'''
    sorted_hands = []
    # sort hands into sorted_power, weakest at 0, highest at -1
    while True:
        if len(sorted_hands) == len(power):
            break
        for hand in power:
            # do not add hands twice
            if hand in sorted_hands:
                continue
            # the first hand should just be appended
            if not sorted_hands:
                sorted_hands.append(hand)
                continue
            index = None
            for sorted_hand in sorted_hands:
                # expect all hands to be unique
                if sorted_hand == hand:
                    continue
                # compare first card, then second, etc
                if hand_is_better_two(hand, sorted_hand):
                    new_index = sorted_hands.index(sorted_hand)
                    if not index:
                        index = new_index
                        continue
                    if new_index > index:
                        index = new_index
            if index is None:
                # insert at first index if hand is the worst
                sorted_hands.insert(0, hand)
            else:
                # +1 because better has higher index
                sorted_hands.insert(index+1, hand)
    return sorted_hands


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


def get_ranks_two(hands: list[tuple[str, int, int]]) -> list[int]:
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
        sorted_hands.append(order_power_two(power))
    # this only works if sorted_hands only contains lists!!
    sorted_hands = [hand for hands in sorted_hands for hand in hands]
    bids_with_ranks = []
    # collect bid * rank for each hand
    for rank in range(1, len(sorted_hands)+1, 1):
        # rank 1 is index 0! thus -1
        bids_with_ranks.append(sorted_hands[rank-1][1] * rank)
    return bids_with_ranks


def solve_part_one(hands: list[tuple[str, int]]):
    return sum(get_ranks(set_hands_power(hands)))


def solve_part_two(hands: list[tuple[str, int]]):
    return sum(get_ranks_two(set_hands_power_two(hands)))


if __name__ == '__main__':
    print('Day 7:')
    day7_input = join(dirname(dirname(__file__)), 'input', 'day7.input')
    day7_hands = read_input(day7_input)
    print(f'part one: {solve_part_one(day7_hands)}')
    day7_hands = read_input(day7_input)
    print(f'part two: {solve_part_two(day7_hands)}')
