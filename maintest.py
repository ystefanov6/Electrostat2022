import asyncio

import matplotlib.pyplot as plt
import numpy as np
from tkinter import *


class App:
    def __init__(self, parent, val, val2, val3, val4, val5, val6, val7, val8, gg, lenX, lenY, X, Y, T):
        self.parent = parent

        self.val = val
        self.val2 = val2
        self.val3 = val3
        self.val4 = val4
        self.val5 = val5
        self.val6 = val6
        self.val7 = val7
        self.val8 = val8
        self.gg = gg
        self.lenX = lenX
        self.lenY = lenY
        self.X = X
        self.Y = Y
        self.T = T

        self.label = Label(text=f'Delta value:')
        self.label.pack(side = LEFT, expand = True, fill = 'x')

        self.entry = Entry(self.parent)
        self.entry.pack(side = LEFT, expand = True, fill = 'x')

        self.label2 = Label(text="Length:")
        self.label2.pack(side = LEFT, expand = True, fill = 'x')

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
        self.button.pack()

        self.ggbutton = Button(text="Compute", command=self.guess_gridd)
        self.ggbutton.pack(side=BOTTOM)

    def use_entry(self):
        contents = self.entry.get()
        self.val = contents

        length = self.entry2.get()
        self.val2 = length
        self.lenX = self.lenY = length

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

    def guess_gridd(self):
        guess_grid = np.empty((int(self.val2), int(self.val2)))
        guess_grid.fill(self.val3)
        self.gg = guess_grid
        guess_grid[(int(self.lenY) - 1):, :] = self.val4
        guess_grid[:1, :] = self.val5
        guess_grid[:, (int(self.lenX) - 1):] = self.val6
        guess_grid[:, :1] = self.val7
        self.grid_creator()

    def grid_creator(self):
        X, Y = np.meshgrid(np.arange(0, int(self.val2)), np.arange(0, int(self.val2)))
        self.X, self.Y = X, Y
        self.finite_diff_method()

    def finite_diff_method(self):
        T = self.gg
        for iter in range(0, int(self.val8)):  # how many times you want to iterate, the bigger the better but slower.
            for i in range(1, int(self.lenX) - 1, int(self.val)):
                for j in range(1, int(self.lenY) - 1, int(self.val)):
                    T[i, j] = 0.25 * (T[i + 1][j] + T[i - 1][j] + T[i][j + 1] + T[i][j - 1])
                    #  This is the actual finite difference approximation formila
        self.T = T
        self.plotter()

    def plotter(self):
        color_interpolation = 50
        colour_map = plt.cm.jet
        plt.title("Potential plot for coaxial cylinders")
        plt.contourf(self.X, self.Y, self.T, color_interpolation, cmap=colour_map)
        plt.colorbar()
        plt.show()


async def main():
    root = Tk()
    root.title("Laplace Numerical Solver")
    root.geometry('800x400')
    root['bg'] = '#ffffff'
    App(root, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    root.mainloop()

if __name__ == '__main__':
    asyncio.run(main())

