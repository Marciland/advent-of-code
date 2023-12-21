'''general functions'''
from dataclasses import dataclass


def get_product(numbers: list[int]) -> int:
    '''returns the product of all numbers'''
    result = 1
    for number in numbers:
        result *= number
    return result


@dataclass
class Point:
    '''2D point'''
    x: int
    y: int
