'''https://adventofcode.com/2023/day/16'''
from multiprocessing import Pool
from os.path import dirname, join
from time import perf_counter

from helpers import Point

RIGHT = Point(x=1, y=0)
LEFT = Point(x=-1, y=0)
UP = Point(x=0, y=-1)
DOWN = Point(x=0, y=1)


def read_input(file_path: str) -> dict[Point]:
    '''formats the day16.txt'''
    contraption = {}
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        rows = [line.strip() for line in file_handle.readlines()]
    for y_index, row in enumerate(rows):
        for x_index in range(0, len(row), 1):
            contraption.update({Point(y=y_index, x=x_index): row[x_index]})
    return contraption


def beam_ended(position: Point, max_position: Point) -> bool:
    '''beam ends if it leaves the contraption -> negative or higher than bounds'''
    if position.x < 0:
        return True
    if position.y < 0:
        return True
    if position.x > max_position.x:
        return True
    if position.y > max_position.y:
        return True
    return False


def handle_backslash(current_position: Point,
                     current_direction: Point) -> tuple[Point, Point] | None:
    '''decide where the beam should move on backslash'''
    if current_direction == RIGHT:
        current_direction = DOWN
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == LEFT:
        current_direction = UP
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == UP:
        current_direction = LEFT
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == DOWN:
        current_direction = RIGHT
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    return None


def handle_slash(current_position: Point,
                 current_direction: Point) -> tuple[Point, Point] | None:
    '''decide where the beam should move on slash'''
    if current_direction == RIGHT:
        current_direction = UP
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == LEFT:
        current_direction = DOWN
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == UP:
        current_direction = RIGHT
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    if current_direction == DOWN:
        current_direction = LEFT
        current_position = current_position.add(current_direction)
        return current_position, current_direction
    return None


def handle_minus(current_position: Point, current_direction: Point,
                 contraption: dict[Point], energized: set[Point],
                 splits_taken: list[Point]) -> tuple[Point, Point, set[Point]] | None:
    '''decide where the beam should move on minus'''
    if current_direction == RIGHT:
        current_position = current_position.add(current_direction)
        return current_position, current_direction, energized
    if current_direction == LEFT:
        current_position = current_position.add(current_direction)
        return current_position, current_direction, energized
    if current_direction == UP:
        if current_position not in splits_taken:
            splits_taken.append(current_position)
            energized = run_beam(current_position.add(LEFT), LEFT,
                                 contraption, energized, splits_taken)
            current_direction = RIGHT
            current_position = current_position.add(current_direction)
            return current_position, current_direction, energized
    if current_direction == DOWN:
        if current_position not in splits_taken:
            splits_taken.append(current_position)
            energized = run_beam(current_position.add(RIGHT), RIGHT,
                                 contraption, energized, splits_taken)
            current_direction = LEFT
            current_position = current_position.add(current_direction)
            return current_position, current_direction, energized
    return None, None, energized


def handle_pipe(current_position: Point, current_direction: Point,
                contraption: dict[Point], energized: set[Point],
                splits_taken: list[Point]) -> tuple[Point, Point, set[Point]] | None:
    '''decide where the beam should move on pipe'''
    if current_direction == RIGHT:
        if current_position not in splits_taken:
            splits_taken.append(current_position)
            energized = run_beam(current_position.add(UP), UP,
                                 contraption, energized, splits_taken)
            current_direction = DOWN
            current_position = current_position.add(current_direction)
            return current_position, current_direction, energized
    if current_direction == LEFT:
        if current_position not in splits_taken:
            splits_taken.append(current_position)
            energized = run_beam(current_position.add(DOWN), DOWN,
                                 contraption, energized, splits_taken)
            current_direction = UP
            current_position = current_position.add(current_direction)
            return current_position, current_direction, energized
    if current_direction == UP:
        current_position = current_position.add(current_direction)
        return current_position, current_direction, energized
    if current_direction == DOWN:
        current_position = current_position.add(current_direction)
        return current_position, current_direction, energized
    return None, None, energized


def run_beam(start_position: Point, start_direction: Point, contraption: dict[Point],
             energized: set[Point], splits_taken: list[Point]) -> set[Point]:
    '''run a beam through the contraption. save energized points'''
    current_position = start_position
    current_direction = start_direction
    while True:
        if beam_ended(current_position, list(contraption)[-1]):
            break
        energized.add(current_position)
        if contraption[current_position] == '.':
            current_position = current_position.add(current_direction)
            continue
        if contraption[current_position] == '\\':
            current_position, current_direction = handle_backslash(current_position,
                                                                   current_direction)
            continue
        if contraption[current_position] == '/':
            current_position, current_direction = handle_slash(current_position,
                                                               current_direction)
            continue
        if contraption[current_position] == '-':
            current_position, current_direction, energized = handle_minus(current_position,
                                                                          current_direction,
                                                                          contraption,
                                                                          energized,
                                                                          splits_taken)
            if current_position is None:
                break
            continue
        if contraption[current_position] == '|':
            current_position, current_direction, energized = handle_pipe(current_position,
                                                                         current_direction,
                                                                         contraption,
                                                                         energized,
                                                                         splits_taken)
            if current_position is None:
                break
            continue
    return energized


def test_position(contraption: dict[Point], position: tuple[Point, Point]) -> int:
    '''run beam from position (start_location + direction) and return len(energized)'''
    current_position = position[0]
    current_direction = position[1]
    # sets will not add duplicates
    energized = set()
    splits_taken = []
    energized = run_beam(current_position, current_direction,
                         contraption, energized, splits_taken)
    return len(energized)


def generate_locations(contraption: dict[Point], start_direction: Point) -> list[tuple]:
    '''generate a list of all possible starting locations and all possible starting directions'''
    locations = []
    max_position = list(contraption)[-1]
    # append possible start positions and start directions with the contraption to the starmap
    # skip unnecessary
    for start_position in contraption:
        if start_position.x == 0 and start_direction == LEFT:
            continue
        if start_position.x == max_position.x and start_direction == RIGHT:
            continue
        if start_position.y == 0 and start_direction == UP:
            continue
        if start_position.y == max_position.y and start_direction == DOWN:
            continue
        point_to_the_left = Point(x=start_position.x-1,
                                  y=start_position.y)
        point_to_the_right = Point(x=start_position.x+1,
                                   y=start_position.y)
        point_above = Point(x=start_position.x,
                            y=start_position.y-1)
        point_below = Point(x=start_position.x,
                            y=start_position.y+1)
        if start_direction == RIGHT and \
            (contraption, (point_to_the_left, RIGHT)) in locations and\
                contraption[point_to_the_left] in ['.', '-']:
            continue
        if start_direction == LEFT and \
            (contraption, (point_to_the_right, LEFT)) in locations and\
                contraption[point_to_the_right] in ['.', '-']:
            continue
        if start_direction == DOWN and \
            (contraption, (point_above, DOWN)) in locations and\
                contraption[point_above] in ['.', '|']:
            continue
        if start_direction == UP and \
            (contraption, (point_below, UP)) in locations and\
                contraption[point_below] in ['.', '|']:
            continue
        locations.append((contraption, (start_position, start_direction)))
    return locations


def solve_part_one(contraption: dict[Point]) -> int:
    '''
    empty space (.) -> same direction
    mirrors (/ and \\) -> reflected
    splitters (| and -) -> pointy end of a splitter: like empty space,
                           flat side of a splitter -> split into two beams
    A tile is energized if that tile has at least one beam
    '''
    # start at top left, heading right
    current_direction = RIGHT
    current_position = Point(x=0, y=0)
    # sets will not add duplicates
    energized = set()
    splits_taken = []
    energized = run_beam(current_position, current_direction,
                         contraption, energized, splits_taken)
    print(len(energized))


def solve_part_two(contraption: dict[Point]):
    '''find beam start position with most energized tiles'''
    possible_directions = [RIGHT, LEFT, UP, DOWN]
    starmap = []
    for start_direction in possible_directions:
        starmap.append((contraption, start_direction))
    with Pool() as pool:
        locations = pool.starmap(generate_locations, starmap)
        locations = [location for ls in locations for location in ls]
        energized = pool.starmap(test_position, locations)
    print(max(energized))


def solve():
    print('Day 16:')
    day16_input = join(dirname(dirname(__file__)), 'input', 'day16.txt')
    print('part one: ', end='')
    start_time = perf_counter()
    contraption = read_input(day16_input)
    solve_part_one(contraption)
    print('solved in:', perf_counter() - start_time)
    print('part two: ', end='')
    start_time = perf_counter()
    contraption = read_input(day16_input)
    solve_part_two(contraption)
    print('solved in:', perf_counter() - start_time)
