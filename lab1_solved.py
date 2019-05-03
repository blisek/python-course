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


#1 calculate & print the value of function y = 2x^2 + 2x + 2 for x=[56, 57, ... 100] (0.5p)
def task1():
    func_str = '2*(x*x) + 2*x + 2'
    print(f'f(x) = {func_str}', flush=True)
    func = parse_math_func(func_str)
    results = [(arg, func(arg)) for arg in range(56, 101)]
    print(', '.join(map(lambda x: f'f({x[0]})={x[1]}', results)))


def _task2_my_factorial(num: int):
    if num == 0:
        return 1
    elif num < 0:
        raise ValueError(f'factorial from number less than 1 ({num})')
    fact = 1
    while num > 1:
        fact *= num
        num -= 1
    return fact


#2 ask the user for a number and print its factorial (1p)
#the length of a chart is the input to your script. The output is a plot (it doesn't matter if it's a y=x or y=e^x+2x or y=|x| function, use your imagination)
#test your solution properly. Look how it behaves given different input values. (1p)
def task2():
    try:
        input_num = int(input('Give number:'))
        # factorial = math.factorial(input_num)
        factorial = _task2_my_factorial(input_num)
        print(f'Factorial of {input_num}: {factorial}')
    except ValueError as e:
        print('Invalid input: ', e)


#3 write a function which takes an array of numbers as an input and finds the lowest value. Return the index of that element and its value (1p)
def task3(*args):
    '''
    :param args: list of arguments convertable to int
    :return: first occurence of min value in array
    '''
    try:
        index, value = min(enumerate(args), key=lambda x: int(x[1]))
        min_vals = [el[0] for el in enumerate(args) if el[1] == value]
        print(f'Lowest value: {min_vals} with index: {index}')
    except ValueError as e:
        print('Invalid input: ', e)


#4 looking at lab1-input and lab1-plot files create your own python script that takes a number and returns any chart of a given length.
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
    x_axis = np.linspace(-length, length, length*5)
    y_axis = f(x_axis)
    xlabel('x')
    ylabel(f'f(x) = {f_def}')
    plot(x_axis, y_axis, 'g:', linewidth=2, markersize=3)
    show()


#5 upload the solution as a Github repository. I suggest creating a directory for the whole python course and subdirectories lab1, lab2 etc. (0.5p)
#Ad 5 Hint write in Google "how to create a github repo". There are plenty of tutorials explaining this matter.
@click.command()
@click.option('--task', default='task1', type=click.Choice(['task1', 'task2', 'task3', 'task4']))
@click.argument('args', nargs=-1)
def select_task(task, args):
    getattr(sys.modules[__name__], task)(*args)


if __name__ == '__main__':
    select_task()
