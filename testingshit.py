import matplotlib.pyplot as plt
import numpy as np
import math
from skimage import draw
from matplotlib.pyplot import plot


def guess_gridd(length, initial_guess):
    guess_grid = np.empty((length, length))
    guess_grid.fill(initial_guess)
    return guess_grid


def main():

    """length = 10
    r = 10
    a = b = length/2
    guess_grid = guess_gridd(length, 0)
    # draw the circle
    for angle in range(0, 360, 1):
        x = r * math.sin(math.radians(angle)) + a
        y = r * math.cos(math.radians(angle)) + b
        guess_grid[int(x), int(y)] = 1

    print(guess_grid)"""
    xx, yy = np.mgrid[:20, :20]
    circle = (xx - 50) ** 2 + (yy - 50) ** 2
    donut = (circle < (2500+50)) & (circle > (2500-50))
    print(donut)
    plt.imshow(donut)
    plt.show()

if __name__ == '__main__':
    main()