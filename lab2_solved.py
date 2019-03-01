import yaml
import math
import sys
import click
import typing
import decimal
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def task0(yml_path: str):
    with open(yml_path, 'r') as f:
        parsed_inputs = yaml.load(f)
        if not parsed_inputs:
            return
        parsed_inputs = list(parsed_inputs)
    print('Parsed inputs: ', parsed_inputs)


def task1(x_radius: float, y_radius: float):
    try:
        x_radius, y_radius = float(x_radius), float(y_radius)
        print(f'r[x] = {x_radius}, r[y] = {y_radius}')
        for val in [x_radius, y_radius]:
            if not val:
                print('Liczba wynosi 0')
                return
            elif math.isinf(val):
                print('Liczba nieskończona')
                return
            elif math.isnan(val):
                print('Niepoprawna liczba')
                return
    except ValueError:
        print(f'Niepoprawne parametry wejściowe: {x_radius}, {y_radius}')
        return
    perimeter = 2.0 * math.pi * x_radius
    field = math.pi * (y_radius ** 2)
    print(f'Perimeter - {perimeter}, field - {field}')


def _task2_find(x: int, y: int):
    if x is None and y is None:
        print(f'x = {x}, y = {y}')
    elif x is None:
        if y % 2 != 0:
            print(f'y = {y} is not even!')
        else:
            print(f'x = {y*2}, y = {y}')
    elif y is None:
        if x % 2 != 0:
            print(f'x = {x} is not even!')
        elif x == 0:
            print('x = 0, y = 2')
        else:
            for possible_divisor in range(x, 0, -1):
                if possible_divisor % 2 == 0 and x % possible_divisor == 0:
                    print(f'x = {x}, y = {possible_divisor}')
                    return
            print(f'Divisor for x = {x} not found')
    else:
        if x % 2 != 0:
            print(f'x = {x} is not even')
        elif y % 2 != 0:
            print(f'y = {y} is not even')
        elif x % y != 0:
            print(f'x = {x} is not divisible by y = {y}')
        else:
            print(f'x = {x} is divisible by y = {y}')


#2 Find X & Y that satisfy: X is divisible by Y and both X & Y are even. (0.5p)
def task2(x: typing.Optional[str] = None, y: typing.Optional[str] = None):
    try:
        x = int(x) if x is not None else None
        y = int(y) if y is not None else None
    except ValueError:
        print(f'Invalid input arguments: (\'{x}\', \'{y}\')')
    _task2_find(x, y)


#3 Check if X is divisible by Y (do it in one line of code), print 'X is divisible by Y' or 'X is not divisible by Y'. (1p)
def task3(x: typing.Optional[str] = None, y: typing.Optional[str] = None):
    try:
        print(f'x = {x} is divisible by y = {y}' if int(x) % int(y) == 0 else f'x = {x} is not divisible y = {y}')
    except ValueError:
        print(f'Invalid input arguments: ({x}, {y})')


#4 Add rounding for the above x/y operation. Round to 2 decimal points. Hint: look up in Google "python limiting number of decimals". (1p)
def task4(x: str, y: str):
    decimal.getcontext().prec = 2
    try:
        print('{0:.2f}'.format(decimal.Decimal(x) / decimal.Decimal(y)))
    except ValueError:
        print(f'Invalid input arguments: ({x}, {y})')


#5 Look at lab2-plot.py and create your own script which takes a number as an input and plots the same 3D wave but with different characteristics
def task5():
    x_knots = np.linspace(-3 * np.pi, 3 * np.pi, 201)
    y_knots = np.linspace(-3 * np.pi, 3 * np.pi, 201)
    X, Y = np.meshgrid(x_knots, y_knots)
    R = np.sqrt(X ** 2 + Y ** 2)
    # Z = np.cos(R) ** 2 * np.exp(-0.1 * R)
    Z = np.cos(R) ** 2 * np.log2(2 + R)
    ax = Axes3D(plt.figure(figsize=(8, 5)))
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.coolwarm, linewidth=0.4)
    plt.show()


@click.command()
@click.option('--task', default='')
@click.argument('arguments', nargs=-1)
def cli_interface(task, arguments):
    current_module = sys.modules[__name__]
    if not task or not hasattr(current_module, task):
        print(f'Nie znaleziono rozwiązania o nazwie: {task}')
        return
    getattr(current_module, task)(*arguments)


if __name__ == '__main__':
    cli_interface()
