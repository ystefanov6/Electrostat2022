import asyncio

import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import math

class App:
    def __init__(self, parent, val, val2, val3, val4, rad2, circle1, circle2, gg, val8, empty, length, X, Y, T):
        self.parent = parent

        self.val = val
        self.val2 = val2
        self.val3 = val3
        self.val4 = val4
        self.val8 = val8
        self.empty = empty
        self.length = length
        self.circle1 = circle1
        self.circle2 = circle2
        self.rad2 = rad2
        self.gg = gg
        self.X = X
        self.Y = Y
        self.T = T

        self.label = Label(text=f'Delta value: (default = 1)')
        self.label.pack()

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
        self.BClabel.pack(fill='x', pady=20)

        self.TopBC = Label(text="Input Radius")
        self.TopBC.pack()

        self.entry4 = Entry(self.parent)
        self.entry4.pack()

        self.radius2 = Label(text="Input Radius 2")
        self.radius2.pack()

        self.rad2 = Entry(self.parent)
        self.rad2.pack()

        self.iter = Label(text="Number of iterations:")
        self.iter.pack()

        self.entry8 = Entry(self.parent)
        self.entry8.pack()

        self.next_func = self.use_entry

        self.ggbutton = Button(text="Compute", command=self.use_entry)
        self.ggbutton.pack()

    def use_entry(self):
        contents = self.entry.get()
        if contents != '':
            self.val = contents
        else:
            self.val = 1

        length = self.entry2.get()
        self.val2 = length

        initial_guess = self.entry3.get()
        self.val3 = initial_guess

        radius = self.entry4.get()
        self.val4 = radius

        iterations = self.entry8.get()
        self.val8 = iterations
        self.iterlabel = Label(self.parent, text=f"Computing for {self.val8} iterations...", bg="#ffffff")
        self.iterlabel.pack()
        self.create_empty()

    def create_empty(self):
        length = int(self.val2) + 1
        self.length = length
        empty = np.zeros((length, length))
        self.empty = empty
        #print(self.empty)

        self.create_circle()

    def create_circle(self):
        """r = int(self.val4)
        a = b = (self.length - 1) / 2
        # draw the circle
        for angle in range(0, 360, 1):
            x = r * math.sin(math.radians(angle)) + a
            y = r * math.cos(math.radians(angle)) + b
            self.empty[int(x), int(y)] = int(self.val3)

        self.circle1 = self.empty"""
        rad = int(self.val4)
        xx, yy = np.mgrid[:int(self.length), :int(self.length)]
        circle = (xx - rad) ** 2 + (yy - rad) ** 2
        donut = (circle < rad**2 + rad+50) &\
                (circle > rad**2 - rad-50)
        self.circle1 = donut
        self.create_circle2()

    def create_circle2(self):
        """r = int(self.rad2.get())
        a = b = (self.length - 1) / 2
        # draw the circle
        for angle in range(0, 360, 1):
            x = r * math.sin(math.radians(angle)) + a
            y = r * math.cos(math.radians(angle)) + b
            self.empty[int(x), int(y)] = 1

        self.circle2 = self.empty"""
        rad = int(self.rad2.get())
        xx, yy = np.mgrid[:int(self.length), :int(self.length)]
        circle = (xx - rad-self.length/4) ** 2 + (yy - rad-self.length/4) ** 2
        donut = (circle < (rad**2) + rad+50) &\
                (circle > (rad**2) - rad-50)
        self.circle2 = donut

        self.boundary_compiler()

    def boundary_compiler(self):
        self.gg = np.add(self.circle1, self.circle2)

        self.grid_creator()

    def grid_creator(self):
        X, Y = np.meshgrid(np.arange(0, int(self.length)), np.arange(0, int(self.length)))
        self.X, self.Y = X, Y
        self.finite_diff_method()

    def finite_diff_method(self):
        T = self.gg
        for iter in range(0, int(self.val8)):  # how many times you want to iterate, the bigger the better but slower.
            for i in range(1, int(self.length) - 1, int(self.length)):
                if i is True:
                    pass
                    for j in range(1, int(self.length) - 1, int(self.val)):
                        if j is True:
                            pass
                            T[i, j] = 0.25 * (T[i + 1][j] + T[i - 1][j] + T[i][j + 1] + T[i][j - 1])
                            #  This is the actual finite difference approximation formula

        self.T = T
        self.plotter()

    def plotter(self):
        color_interpolation = 50
        colour_map = plt.cm.jet
        plt.title("Potential plot for coaxial cylinders")
        plt.contourf(self.X, self.Y, self.T, color_interpolation, cmap=colour_map)
        plt.colorbar()
        plt.show()
        self.iterlabel.pack_forget()


def main():
    root = Tk()
    root.title("Laplace Numerical Solver")
    root.geometry('800x450')
    root['bg'] = '#ffffff'
    App(root, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    root.mainloop()


if __name__ == '__main__':
    main()

