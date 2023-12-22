'''https://adventofcode.com/2023/'''
import importlib
import sys
from argparse import ArgumentParser

solved_days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', '--skip', dest='skip')
    parser.add_argument('-x', '--execute', dest='exe')
    args = parser.parse_args()
    if args.exe:
        if int(args.exe) in solved_days:
            imported_day = importlib.import_module(f'solution.day{args.exe}')
            imported_day.solve()
            sys.exit(0)
    skip_list = []
    if args.skip:
        skip_list = [int(x) for x in args.skip.split(',')]
    for day in solved_days:
        if day in skip_list:
            continue
        imported_day = importlib.import_module(f'solution.day{day}')
        imported_day.solve()
