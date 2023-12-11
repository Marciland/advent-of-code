'''https://adventofcode.com/2023/day/2'''
import os

from helpers import get_sum

day1_input = os.path.join(os.getcwd(), 'day2.txt')
MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14


def read_input() -> dict[int, list[dict]]:
    '''formats the day2.txt'''
    games_dict = {}
    with open(day1_input, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    for line in file_content:
        game_sets = []
        game_id = int(line.split(':')[0].split(' ')[1])
        for game_set in line.split(':')[1].split(';'):
            set_string = game_set.replace('\n', '').strip()
            new_set = {}
            for color in set_string.split(','):
                color = color.strip()
                if 'red' in color:
                    new_set.update({'red': int(color.split(' ')[0])})
                if 'green' in color:
                    new_set.update({'green': int(color.split(' ')[0])})
                if 'blue' in color:
                    new_set.update({'blue': int(color.split(' ')[0])})
            game_sets.append(new_set)
        games_dict.update({game_id: game_sets})
    return games_dict


def set_valid(game_set: dict) -> bool:
    '''check if a set is valid'''
    for color, amount in game_set.items():
        if color == 'red' and amount > MAX_RED:
            return False
        if color == 'green' and amount > MAX_GREEN:
            return False
        if color == 'blue' and amount > MAX_BLUE:
            return False
    return True


def game_valid(game_sets: list[dict]) -> bool:
    '''check if game is valid'''
    for game_set in game_sets:
        if not set_valid(game_set):
            return False
    return True


def get_valid_game_ids(games: dict[int, list[dict]]) -> list[int]:
    '''takes all games and returns the valid ids'''
    valid_games = []
    for game_id, game_sets in games.items():
        if game_valid(game_sets):
            valid_games.append(game_id)
    return valid_games


def find_fewest_necessary(game_sets: list[dict]) -> dict:
    '''returns the fewest necessary for a game (game_sets of a game)'''
    highest_red = 0
    highest_green = 0
    highest_blue = 0
    for game_set in game_sets:
        for color, amount in game_set.items():
            if color == 'red' and highest_red < amount:
                highest_red = amount
            if color == 'green' and highest_green < amount:
                highest_green = amount
            if color == 'blue' and highest_blue < amount:
                highest_blue = amount
    return {'red': highest_red, 'green': highest_green, 'blue': highest_blue}


def get_fewest_cubes(games: dict[int, list[dict]]) -> list[dict]:
    '''gets the fewest necessary cubes for each game'''
    fewest_cubes = []
    for _, game_sets in games.items():
        test = find_fewest_necessary(game_sets)
        fewest_cubes.append(test)
    return fewest_cubes


def get_powers(games: list[dict]) -> list[int]:
    '''multiply red*green*blue for each game'''
    powers = []
    for game in games:
        power = 1
        for _, amount in game.items():
            power = power * amount
        powers.append(power)
    return powers


print(get_sum(get_valid_game_ids(read_input())))  # part one
print(get_sum(get_powers(get_fewest_cubes(read_input()))))  # part two
