'''general functions'''
from dataclasses import dataclass


def get_product(numbers: list[int]) -> int:
    '''returns the product of all numbers'''
    result = 1
    for number in numbers:
        result *= number
    return result


@dataclass
class Galaxy:
    '''2D point'''
    x: int
    y: int


@dataclass(frozen=True, eq=True, order=True)
class Point:
    '''2D point'''
    y: int
    x: int

    def add(self, other_point):
        '''x+other.x, y+other.y'''
        return Point(x=self.x + other_point.x, y=self.y + other_point.y)
