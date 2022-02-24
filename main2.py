import asyncio

import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import math


class App:
    def __init__(self, parent, val, val2, val3, val4, val5, val6, val7, val8):
        self.parent = parent

        self.label = Label(text=f'Delta value:')
        self.label.pack()

        self.val = val
        self.val2 = val2
        self.val3 = val3
        self.val4 = val4
        self.val5 = val5
        self.val6 = val6
        self.val7 = val7
        self.val8 = val8

        self.entry = Entry(self.parent)
        self.entry.pack()

        self.label2 = Label(text="Length:")
        self.label2.pack()

        self.entry2 = Entry(self.parent)
        self.entry2.pack()

        self.label3 = Label(text="Initial guess:")
        self.label3.pack()

        self.entry3 = Entry(self.parent)
        self.entry3.pack()

        self.BClabel = Label(text="BOUNDARY CONDITIONS")
        self.BClabel.pack(fill='x')

        self.TopBC = Label(text="Top boundary condition:")
        self.TopBC.pack()

        self.entry4 = Entry(self.parent)
        self.entry4.pack()

        self.BotBC = Label(text="Bottom boundary condition:")
        self.BotBC.pack()

        self.entry5 = Entry(self.parent)
        self.entry5.pack()

        self.RightBC = Label(text="Right boundary condition:")
        self.RightBC.pack()

        self.entry6 = Entry(self.parent)
        self.entry6.pack()

        self.LeftBC = Label(text="Left boundary condition:")
        self.LeftBC.pack()

        self.entry7 = Entry(self.parent)
        self.entry7.pack()

        self.iter = Label(text="Number of iterations:")
        self.iter.pack()

        self.entry8 = Entry(self.parent)
        self.entry8.pack()

        self.next_func = self.use_entry

        self.button = Button(parent, text='OK', command=self.use_entry)
        self.button.pack(side=BOTTOM)

    def use_entry(self):
        contents = self.entry.get()
        self.val = contents

        length = self.entry2.get()
        self.val2 = length

        initial_guess = self.entry3.get()
        self.val3 = initial_guess

        top_boundary = self.entry4.get()
        self.val4 = top_boundary

        bottom_boundary = self.entry5.get()
        self.val5 = bottom_boundary

        right_boundary = self.entry6.get()
        self.val6 = right_boundary

        left_boundary = self.entry7.get()
        self.val7 = left_boundary

        iterations = self.entry8.get()
        self.val8 = iterations


def guess_gridd(length, initial_guess):
    guess_grid = np.empty((length, length))
    guess_grid.fill(initial_guess)
    return guess_grid


def grid_creator(length):
    X, Y = np.meshgrid(np.arange(0, length), np.arange(0, length))
    return X, Y


def finite_diff_method(lenX, lenY, guess_grid, delta, iterations):
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


async def main():
    root = Tk()
    root.title("Laplace Numerical Solver")
    root.geometry('800x400')
    root['bg'] = '#ffffff'
    app = App(root, 0, 0, 0, 0, 0, 0, 0, 0)
    root.mainloop()
    #  Setting constants and Boundary Conditions
    delta = int(app.val)
    length = int(app.val2)
    lenX = lenY = length

    length = 21
    r = 10
    a = b = length / 2
    guess_grid = guess_gridd(length, 0)
    # draw the circle
    for angle in range(0, 360, 5):
        x = r * math.sin(math.radians(angle)) + a
        y = r * math.cos(math.radians(angle)) + b
        guess_grid[int(x), int(y)] = 1

    print(guess_grid)
    print(guess_grid)
    mesh_grid = grid_creator(length)
    potential = finite_diff_method(lenX, lenY, guess_grid, delta, 300)
    plotter(mesh_grid[0], mesh_grid[1], potential)


if __name__ == '__main__':
    asyncio.run(main())

