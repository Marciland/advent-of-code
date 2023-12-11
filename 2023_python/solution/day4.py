'''https://adventofcode.com/2023/day/4'''
from os.path import dirname, join


def read_input(file_path: str) -> list:
    '''formats the day4.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
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


def solve_part_one(cards: list):
    return sum(get_points_per_card(cards))


def solve_part_two(cards: list):
    return sum(get_cards_total(cards))


if __name__ == '__main__':
    print('Day 4:')
    day4_input = join(dirname(dirname(__file__)), 'input', 'day4.input')
    day4_cards = read_input(day4_input)
    print(f'part one: {solve_part_one(day4_cards)}')
    day4_cards = read_input(day4_input)
    print(f'part two: {solve_part_two(day4_cards)}')
