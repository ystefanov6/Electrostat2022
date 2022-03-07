import numpy as np
import matplotlib.pyplot as plt


def create_rectangle(length, x, y, x_off, y_off):
    grid = np.zeros((length, length), dtype=bool)
    # grid[x_off:x+x_off, y_off:y+y_off] = True
    grid[y_off:y + y_off, x_off:x + x_off] = True

    return grid

def create_circle_boundary(rad, length):
    x, y = np.mgrid[:length, :length]
    circle = (x - rad * (length / 2 / rad)) ** 2 +\
             (y - rad * (length / 2 / rad)) ** 2
    donut = (circle < rad ** 2 + rad + length / 4) & \
            (circle > rad ** 2 - rad - length / 4)

    return donut


def create_circle_boundary2(rad2, length):
    x, y = np.mgrid[:length, :length]
    circle = (x - rad2 * (length / 2 / rad2)) ** 2 + (y - rad2 * (length / 2 / rad2)) ** 2
    donut = (circle < rad2 ** 2 + rad2 + length / 4) & \
            (circle > rad2 ** 2 - rad2 - length / 4)

    return donut


def boundary_comp(circle1, circle2):
    boundaries = np.add(circle1, circle2)

    return boundaries


def create_value_grid(circle1, circle2, length, init_guess):

    temp_grid2 = np.zeros((length, length))
    temp_grid = np.zeros((length, length))
    for i in range(0, length):
        for j in range(0, length):
            if circle1[i][j]:
                temp_grid[i][j] = init_guess

    for i in range(0, length):
        for j in range(0, length):
            if circle2[i][j]:
                temp_grid2[i][j] = 1

    return np.add(temp_grid, temp_grid2)


def finite_diff_method(length, delta, T, T2, iterations):
    for iter in range(0, iterations):
        for i in range(1, length - 1, delta):
            for j in range(1, length - 1, delta):
                if not T[i, j]:
                    T2[i, j] = 0.25 * (T2[i + 1][j] + T2[i - 1][j] + T2[i][j + 1] + T2[i][j - 1])
                else:
                    pass

    return T2


def plotter(FND_result):
    plt.title("Potential plot for coaxial cylinders")
    plt.imshow(FND_result)
    plt.show()


def main():
    length = 100
    rad1 = 50
    rad2 = 25
    delta = 1
    initial_guess = 30
    iterations = 300

    rect = create_rectangle(length, 50, 5, 20, 2)
    plotter(rect)
    """circle1 = create_circle_boundary(rad1, length)
    circle2 = create_circle_boundary(rad2, length)
    boundaries = boundary_comp(circle1, circle2)
    value_grid = create_value_grid(circle1, circle2, length, initial_guess)

    FND_result = finite_diff_method(length, delta, boundaries, value_grid, iterations)
    plotter(FND_result)"""


if __name__ == '__main__':
    main()


