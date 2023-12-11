'''
https://adventofcode.com/2023/day/10

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal!

Circle of pipes:
.....
.F-7.
.|.|.
.L-J.
.....

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF

Every Pipe has exactly 2 other pipes connecting!

you need to find the tile that would take the longest number of steps
along the loop to reach from the starting point

Find the single giant loop starting at S.
How many steps along the loop does it take to get from the starting position
to the point farthest from the starting position?
'''
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


def read_input(file_path: str) -> list[list[str]]:
    '''formats the day10.input'''
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        file_content = file_handle.readlines()
    lines = []
    for line in file_content:
        lines.append(list(line.strip()))
    return lines


def find_start(lines: list) -> Point | None:
    '''search the start point'''
    for y_index in range(0, len(lines), 1):
        if 'S' in lines[y_index]:
            for x_index in range(0, len(lines[y_index]), 1):
                if lines[y_index][x_index] == 'S':
                    return Point(y=y_index, x=x_index)
    return None


def find_possible_steps(field: list[list[str]],
                        current_point: Point) -> tuple[Point, Point]:
    '''finds the next steps'''
    possible_steps = []
    can_go_left = False
    can_go_right = False
    can_go_above = False
    can_go_below = False
    current_symbol = field[current_point.y][current_point.x]
    match (current_symbol):
        case '|':
            can_go_left = False
            can_go_right = False
            can_go_above = True
            can_go_below = True
        case '-':
            can_go_left = True
            can_go_right = True
            can_go_above = False
            can_go_below = False
        case 'L':
            can_go_left = False
            can_go_right = True
            can_go_above = True
            can_go_below = False
        case 'J':
            can_go_left = True
            can_go_right = False
            can_go_above = True
            can_go_below = False
        case '7':
            can_go_left = True
            can_go_right = False
            can_go_above = False
            can_go_below = True
        case 'F':
            can_go_left = False
            can_go_right = True
            can_go_above = False
            can_go_below = True
        case 'S':
            if current_point.x != 0:
                left = field[current_point.y][current_point.x-1]
                match(left):
                    case '|':
                        can_go_left = False
                    case '-':
                        can_go_left = True
                    case 'L':
                        can_go_left = True
                    case 'J':
                        can_go_left = False
                    case '7':
                        can_go_left = False
                    case 'F':
                        can_go_left = True
                    case '.':
                        can_go_left = False
                    case 'S':
                        can_go_left = True
            if current_point.x != len(field[1])-1:
                right = field[current_point.y][current_point.x+1]
                match(right):
                    case '|':
                        can_go_right = False
                    case '-':
                        can_go_right = True
                    case 'L':
                        can_go_right = False
                    case 'J':
                        can_go_right = True
                    case '7':
                        can_go_right = True
                    case 'F':
                        can_go_right = False
                    case '.':
                        can_go_right = False
                    case 'S':
                        can_go_right = True
            if current_point.x != len(field[0])-1:
                above = field[current_point.y-1][current_point.x]
                match(above):
                    case '|':
                        can_go_above = True
                    case '-':
                        can_go_above = False
                    case 'L':
                        can_go_above = False
                    case 'J':
                        can_go_above = False
                    case '7':
                        can_go_above = True
                    case 'F':
                        can_go_above = True
                    case '.':
                        can_go_above = False
                    case 'S':
                        can_go_above = True
            if current_point.y != 0:
                below = field[current_point.y+1][current_point.x]
                match(below):
                    case '|':
                        can_go_below = True
                    case '-':
                        can_go_below = False
                    case 'L':
                        can_go_below = True
                    case 'J':
                        can_go_below = True
                    case '7':
                        can_go_below = False
                    case 'F':
                        can_go_below = False
                    case '.':
                        can_go_below = False
                    case 'S':
                        can_go_below = True
    if can_go_left:
        possible_steps.append(Point(y=current_point.y, x=current_point.x-1))
    if can_go_right:
        possible_steps.append(Point(y=current_point.y, x=current_point.x+1))
    if can_go_above:
        possible_steps.append(Point(y=current_point.y-1, x=current_point.x))
    if can_go_below:
        possible_steps.append(Point(y=current_point.y+1, x=current_point.x))
    return (possible_steps[0], possible_steps[1])


def walk_the_roehre(field: list[list[str]], start_point: Point) -> int:
    '''walk the pipe from start to start'''
    steps = 0
    possible_step1, _ = find_possible_steps(field, start_point)
    current_point = possible_step1
    steps += 1
    last_point = start_point
    while True:
        # wenn wir vor dem Ziel stehen, mach den letzten schritt und hör auf
        if current_point == start_point:
            break
        # finde heraus welche die nächsten schritte sein könnten
        possible_step1, possible_step2 = find_possible_steps(field,
                                                             current_point)
        # setzte den nächsten punkt auf den nicht vorherigen schritt
        if last_point == possible_step1:
            last_point = current_point
            current_point = possible_step2
        if last_point == possible_step2:
            last_point = current_point
            current_point = possible_step1
        # mach einen schritt
        steps += 1
    return steps


def solve_part_one(field: list[list[str]]):
    return walk_the_roehre(field, find_start(field)) // 2


if __name__ == '__main__':
    print('Day 10:')
    day10_input = join(dirname(dirname(__file__)), 'input', 'day10.input')
    day10_field = read_input(day10_input)
    print(f'part one: {solve_part_one(day10_field)}')
    print('part two: WIP')
