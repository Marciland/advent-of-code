'''https://adventofcode.com/2023/day/16'''
from multiprocessing import Pool
from os.path import dirname, join
from dataclasses import dataclass


@dataclass(frozen=True, eq=True, order=True)
class Point:
    '''2D point'''
    y: int
    x: int

    def add(self, other_point):
        '''x+other.x, y+other.y'''
        return Point(x=self.x + other_point.x, y=self.y + other_point.y)


RIGHT = Point(x=1, y=0)
LEFT = Point(x=-1, y=0)
UP = Point(x=0, y=-1)
DOWN = Point(x=0, y=1)


def read_input(file_path: str) -> dict[Point]:
    '''formats the day16.input'''
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


def generate_locations(contraption: dict[Point]) -> list[tuple]:
    '''generate a list of all possible starting locations and all possible starting directions'''
    locations = []
    max_position = list(contraption)[-1]
    # append possible start positions and start directions with the contraption to the starmap
    # skip unnecessary
    for start_position in contraption:
        if start_position.x == 0:
            locations.append((contraption, (start_position, RIGHT)))
            if start_position.y == 0:
                locations.append((contraption, (start_position, DOWN)))
            if start_position.y == max_position.y:
                locations.append((contraption, (start_position, UP)))
            continue
        if start_position.x == max_position.x:
            locations.append((contraption, (start_position, LEFT)))
            if start_position.y == 0:
                locations.append((contraption, (start_position, DOWN)))
            if start_position.y == max_position.y:
                locations.append((contraption, (start_position, UP)))
            continue
        if start_position.y == 0:
            locations.append((contraption, (start_position, DOWN)))
            continue
        if start_position.y == max_position.y:
            locations.append((contraption, (start_position, UP)))
            continue
    return locations


def solve_part_one(contraption: dict[Point]):
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
    return len(energized)


def solve_part_two(contraption: dict[Point]):
    '''find beam start position with most energized tiles'''
    locations = generate_locations(contraption)
    with Pool() as pool:
        energized = pool.starmap(test_position, locations)
    return max(energized)


if __name__ == '__main__':
    print('Day 16:')
    day16_input = join(dirname(dirname(__file__)), 'input', 'day16.input')
    day16_contraption = read_input(day16_input)
    print(f'part one: {solve_part_one(day16_contraption)}')
    day16_contraption = read_input(day16_input)
    print(f'part two: {solve_part_two(day16_contraption)}')
