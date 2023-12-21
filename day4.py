'''https://adventofcode.com/2023/day/4'''
import os

day4_input = os.path.join(os.getcwd(), 'day4.txt')


def read_input() -> list:
    '''formats the day4.txt'''
    with open(day4_input, 'r', encoding='utf-8') as file_handle:
        file_content = [line.strip() for line in file_handle.readlines()]
    cards = []
    for line in file_content:
        winning = (line.split('|')[0].strip())
        winning = winning.split(':')[1].strip()
        winning = [number.strip()
                   for number in winning.split(' ') if number.isnumeric()]
        numbers = (line.split('|')[1].strip())
        numbers = [number.strip()
                   for number in numbers.split(' ') if number.isnumeric()]
        cards.append((winning, numbers))
    return cards


def get_points_per_card(cards: list) -> list[int]:
    '''first match is 1 point, every match afterwards is points*2 e.g. 1*2*2*2 for 4 matches'''
    points_per_card = []
    for card in cards:
        matches = 0
        for number in card[1]:
            if number in card[0]:
                matches += 1
        if matches < 2:
            points_per_card.append(matches)
        else:
            points_per_card.append(1*2**(matches-1))
    return points_per_card


def get_cards_total(cards: list) -> list[int]:
    '''increase amount (weight) of cards at card indexes of matches'''
    amount_of_cards = [1 for _ in range(len(cards))]
    for index in range(0, len(cards), 1):
        matches = 0
        for number in cards[index][1]:
            if number in cards[index][0]:
                matches += 1
        for i in range(1, matches+1, 1):
            amount_of_cards[index+i] += amount_of_cards[index]
    return amount_of_cards


print(sum(get_points_per_card(read_input())))  # part one
print(sum(get_cards_total(read_input())))  # part two
