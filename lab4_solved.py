import numpy as np
import matplotlib.pyplot as plt


def euler_approximation(a: float, h: float, T: float):
    """
    Looking at the Euler method above create your own function which takes upper arguments
    as an input and plots the solution of a differential equation x' = ax (1p)
    :param a: a (from x' = ax)
    :param h: h - step
    :param T: T time range
    :return:
    """
    t_arr = np.arange(0, T, h)
    x_arr = np.zeros(t_arr.shape)
    x_arr[0] = 1.0

    for i in range(t_arr.size - 1):
        x_arr[i+1] = x_arr[i] + h * (a * x_arr[i])

    plt.plot(t_arr, x_arr, 'o')
    plt.xlabel('t', fontsize=24)
    plt.ylabel('x', fontsize=24)
    plt.show()


def euler_approximation_ideal(a: float, h: float, T: float):
    """
    Beside the solution print the 'ideal' approximation on your chart using for example green color as a reference. (1p)
    Hint: use small step value. Use plt.legend to explain which serie is the 'ideal'
    :param a: a (from x' = ax)
    :param h: h - step
    :param T: T time range
    :return:
    """
    b = 0  # x'' + bx' + ax = 0

    t_arr = np.arange(0, T, h)
    x_arr = np.zeros(t_arr.shape)
    y_arr = np.zeros(t_arr.shape)
    x_arr[0], y_arr[0] = 1.0, 0.0

    for i in range(t_arr.size - 1):
        x_arr[i + 1] = x_arr[i] + h * (y_arr[i])
        y_arr[i + 1] = y_arr[i] + h * (-a * x_arr[i+1] - b * y_arr[i])
        # print(f'x_arr[{i+1}] = {x_arr[i+1]}')
        # print(f'y_arr[{i+1}] = {y_arr[i+1]}')

    plt.plot(t_arr, x_arr, 'k', label='x')
    plt.plot(t_arr, y_arr, 'g', label='y')
    plt.xlabel('t', fontsize=20)
    plt.ylabel('state', fontsize=20)
    plt.legend(loc='upper right', fontsize=16)
    plt.show()


if __name__ == '__main__':
    # euler_approximation(1.5, .01, 5)
    euler_approximation_ideal(1.5, .001, 15.0)
