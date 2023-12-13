'''general functions'''


def get_sum(numbers: list[int]) -> int:
    '''sums up the list of numbers'''
    result_sum = 0
    for number in numbers:
        result_sum += number
    return result_sum


def get_product(numbers: list[int]) -> int:
    '''returns the product of all numbers'''
    result = 1
    for number in numbers:
        result *= number
    return result
