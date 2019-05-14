import numpy as np
import matplotlib.pyplot as plt
from scipy import linspace , cos , exp, random, meshgrid, pi, zeros
from scipy.optimize import fmin
import time
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import plot, show, legend, figure, cm, contour, clabel


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


def find_global_optima(func, start_point=(0, 1)):
    x0 = list(start_point)
    curr_x = fmin(func, x0, disp=False)
    curr_val = func(curr_x)
    best_x = curr_x
    best_val = curr_val
    start_time = time.time()
    pointless_counter = 0
    while True:
        x0 = random.randn(2)
        curr_x = fmin(func, x0, disp=False)
        curr_val = func(curr_x)

        if curr_val < best_val:
            best_x = curr_x
            best_val = curr_val
            # pointless_counter = 0
        else:
            pointless_counter += 1

        if (time.time() - start_time) > 30:
            break

        if pointless_counter > 1e3:
            print('pointless_counter:', pointless_counter)
            break
    return best_x, best_val


def optima_in_3d_function(func, *args):
    pass


def test_function(x):
    return (x[0]-2) ** 2 + (x[1]-2) ** 2


def test_function2(x):
    return 20 + x[0] ** 2 - 10 * cos(2*pi*x[0]) +\
        x[1] ** 2 - 10 * cos(2*pi*x[1])


if __name__ == '__main__':
    # euler_approximation(1.5, .01, 5)
    # euler_approximation_ideal(1.5, .001, 15.0)
    # test_func = lambda x: -exp(-x[0] ** 2 - x[1] ** 2)
    print(find_global_optima(test_function2))

    x0 = x_min = [0, 0]

    delta = 6
    x_knots = linspace(x_min[0] - delta, x_min[0] + delta, 41)
    y_knots = linspace(x_min[1] - delta, x_min[1] + delta, 41)
    X, Y = meshgrid(x_knots, y_knots)
    Z = zeros(X.shape)
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            Z[i][j] = test_function2([X[i, j], Y[i, j]])

    ax = Axes3D(figure(figsize=(8, 5)))
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0.4)
    ax.plot([x0[0]], [x0[1]], [test_function2(x0)], color='g', marker='o', markersize=5, label='initial')
    ax.plot([x_min[0]], [x_min[1]], [test_function2(x_min)], color='k', marker='o', markersize=5, label='final')
    ax.legend()
    show()
