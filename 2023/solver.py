'''https://adventofcode.com/2023/'''
import importlib

solved_days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

if __name__ == '__main__':
    for day in solved_days:
        imported_day = importlib.import_module(f'solution.day{day}')
        imported_day.solve()
