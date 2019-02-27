import yaml
import math


def task1():
    with open('lab2_data.yml', 'r') as f:
        parsed_inputs = yaml.load(f)
        if not parsed_inputs:
            return
        parsed_inputs = list(parsed_inputs)
    print('Parsed inputs: ', parsed_inputs)


def task2(x_radius: float, y_radius: float):
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
