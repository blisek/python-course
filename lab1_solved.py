import re
import math
import typing as _t
import numpy as np
import sys
import click
from matplotlib.pyplot import plot, show, xlabel, ylabel


__FUNC_CLEAN_REGEX = re.compile(r'[^x\+\-\*\^/0-9]', re.IGNORECASE)


def parse_math_func(function: str):
    parsed = __FUNC_CLEAN_REGEX.sub('', function)
    return eval(f'lambda x: {parsed}')


def task1():
    func = parse_math_func('2*(x*x) + 2*x + 2')
    results = [(arg, func(arg)) for arg in range(56, 101)]
    print(', '.join(map(lambda x: f'f({x[0]})={x[1]}', results)))


def task2():
    try:
        input_num = int(input('Give number:'))
        factorial = math.factorial(input_num)
        print(f'Factorial of {input_num}: {factorial}')
    except ValueError as e:
        print('Invalid input: ' + e)


def task3(*args):
    index, value = min(enumerate(args), key=lambda x: x[1])
    print(f'Lowest value: {value} with index: {index}')


def task4(length: int):
    try:
        length = int(length)
    except ValueError:
        print(f'Podano nieprawidłową liczbę: {length}')
        return
    if length < 0:
        length = abs(length)
    f_def = '2*(x*x)-1'
    f = parse_math_func(f_def)
    x_axis = np.linspace(.0, length, length*5)
    y_axis = f(x_axis)
    xlabel('x')
    ylabel(f'f(x) = {f_def}')
    plot(x_axis, y_axis, 'g:', linewidth=2, markersize=3)
    show()


@click.command()
@click.option('--task', default='task1', type=click.Choice(['task1', 'task2', 'task3', 'task4']))
@click.argument('args', nargs=-1)
def select_task(task, args):
    getattr(sys.modules[__name__], task)(*args)


if __name__ == '__main__':
    select_task()
