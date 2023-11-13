
from timeit import timeit
from typing import Callable, TypeVar, Sequence, Any, Union

_T = TypeVar('_T')
__T = TypeVar('__T')

DEFAULT_NUMBER = 10_000

def time(function: Callable[[_T], Any], args: Sequence[_T] | None = None, number: int = DEFAULT_NUMBER,
                  average: bool = False, stringify: bool = True) -> str | float:
    """Time in seconds"""

    if args is None: args = []

    value = timeit(lambda: function(*args), number=number)

    if average: value /= number

    return f'Ellapsed Time: {value} seconds' if stringify else value


def compare(function_1: Callable[[_T], Any], function_2: Callable[[__T], Any],
            args_1: Sequence[_T] | None = None, args_2: Sequence[__T] | None = None, 
            number: int = DEFAULT_NUMBER, average: bool = False, stringify: bool = True) -> str | float:
    """Time in seconds"""
    
    if args_1 is None: args_1 = []
    if args_2 is None: args_2 = args_1

    value_1 = timeit(lambda: function_1(*args_1), number=number)
    value_2 = timeit(lambda: function_2(*args_2), number=number)

    if average:
        value_1 /= number
        value_2 /= number

    if not stringify: return value_1, value_2, value_1 / value_2

    time_type = 'average' if average else 'total'

    message = f'Function 1 took: {value_1} seconds ({time_type})\nFunction 2 took: {value_2} seconds ({time_type})\n' + \
              f'Function 1 took {value_1 / value_2} times as much as Function 2'
    
    return message


def time_tests(function: Callable[[_T], Any], tests: Sequence[Sequence[_T]] | None = None, number: int = DEFAULT_NUMBER,
               average: bool = False, stringify: bool = True, complete_stats: bool = False) -> float | str:
    """
    Time in seconds
    
    Return Value:
        individual_times, average_time, min, max
    """

    multiplyer = 1 / number if average else 1

    values = [timeit(lambda: function(*i), number=number) * multiplyer for i in tests]

    value = sum(values) / (len(tests) if average else 1)
    time_type = 'average' if average else 'total'

    if not complete_stats: 
        return f'Ellapsed Time: {value} seconds ({time_type})' if stringify else value
    
    if not stringify:
        return values, value, min(values), max(values)
    
    return f'Individual Times:\n\t{"s, ".join(map(str, values))}\n\nTotal Time: \n\t{sum(values)} ({time_type})\n\n' + \
           f'Average Time: \n\t{sum(values) / len(values)} ({time_type})\n\n' + \
           f'Minimum Time: \n\t{min(values)} ({time_type})\n\nMaximum Time: \n\t{max(values)} ({time_type})'

