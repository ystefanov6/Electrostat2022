import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
window = tk.Tk()


def guess_grid(length):
    guess_grid = np.empty((length, length))
    guess_grid.fill(initial_guess)
    return guess_grid


#  Setting constants and Boundary Conditions
length = 20
delta = int(input("Input desired delta (default 1): ") or "1")
initial_guess = 30  # initial guess of what average potential would look like, the better the guess the faster the conv.
lenX = lenY = length

guess_grid = guess_grid(length)
TopBC = 100
BottomBC = 0
RightBC = 0
LeftBC = 30

guess_grid[(lenY - 1):, :] = TopBC
guess_grid[:1, :] = BottomBC
guess_grid[:, (lenX - 1):] = RightBC
guess_grid[:, :1] = LeftBC


def grid_creator(length):
    X, Y = np.meshgrid(np.arange(0, length), np.arange(0, length))
    return X, Y


def finite_diff_method(lenX, lenY, guess_grid, delta):
    iterations = int(input("Number of iterations: "))
    T = guess_grid
    for iter in range(0, iterations):  # how many times you want to iterate, the bigger the better but slower.
        for i in range(1, lenX - 1, delta):
            for j in range(1, lenY - 1, delta):
                T[i, j] = 0.25 * (T[i + 1][j] + T[i - 1][j] + T[i][j + 1] + T[i][j - 1])
                #  This is the actual finite difference approximation formila
    print(f"Computing for {iterations} iterations, wait a moment...")
    return T


def plotter(X, Y, T):
    color_interpolation = 50
    colour_map = plt.cm.jet
    plt.title("Potential plot for coaxial cylinders")
    plt.contourf(X, Y, T, color_interpolation, cmap=colour_map)
    plt.colorbar()
    plt.show()


def main():
    mesh_grid = grid_creator(length)
    potential = finite_diff_method(lenX, lenY, guess_grid, delta)
    plotter(mesh_grid[0], mesh_grid[1], potential)


if __name__ == '__main__':
    main()

