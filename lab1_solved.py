import re
import math
import typing as _t
import numpy as np
import sys
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


def _task3_lowest(nums: _t.List[_t.Union[int, float]]) -> _t.Tuple[_t.Any, _t.Any]:
    return min(enumerate(nums), key=lambda x: x[1])


def task3():
    sample_values = [5, 9, 1, 2, 4, 99, 13, 19]
    index, value = _task3_lowest(sample_values)
    print(f'Lowest value: {value} with index: {index}')


def _task4_plot(length: int):
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


def task4():
    if len(sys.argv) < 2:
        sys.argv.insert(1, 50)
    _task4_plot(int(sys.argv[1]))


if __name__ == '__main__':
    tasks = [('task1', task1), ('task2', task2), ('task3', task3), ('task4', task4)]
    while True:
        try:
            for inx, task in enumerate(tasks):
                print(f'{inx}] {task[0]}')
            choice = input('Choose: ')
            if not choice or choice.lower() == 'q':
                break
            choice = int(choice)
            choosen_f = tasks[choice]
            print(f'Executing {choosen_f[0]}...')
            choosen_f[1].__call__()
        except:
            continue
