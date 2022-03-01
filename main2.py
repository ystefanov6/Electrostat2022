import matplotlib.pyplot as plt
import numpy as np
from tkinter import *


class App:
    def __init__(self, parent, temp):
        self.parent = parent

        self.delta = temp
        self.length = temp
        self.init_guess = temp
        self.rad1 = temp
        self.rad2 = temp
        self.iterations = temp
        self.circle1 = temp
        self.circle2 = temp
        self.gg = temp
        self.valgrid = temp
        self.T = temp

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

        self.entry5 = Entry(self.parent)
        self.entry5.pack()

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
            self.delta = contents
        else:
            self.delta = 1

        length = self.entry2.get()
        self.length = int(length) + 1

        initial_guess = self.entry3.get()
        self.init_guess = initial_guess

        radius = self.entry4.get()
        self.rad1 = radius

        radius2 = self.entry5.get()
        self.rad2 = radius2

        iterations = self.entry8.get()
        self.iterations = iterations
        self.iterlabel = Label(self.parent, text=f"Computing for {self.iterations} iterations...", bg="#ffffff")
        self.iterlabel.pack()
        self.create_circle_boundary()

    def create_circle_boundary(self):
        rad = int(self.rad1)
        x, y = np.mgrid[:self.length, :self.length]
        circle = (x-rad*(self.length/2/rad))**2 + (y-rad*(self.length/2/rad))**2
        donut = (circle < rad**2 + rad+self.length/4) &\
                (circle > rad**2 - rad-self.length/4)
        self.circle1 = donut
        self.create_circle2_boundary()

    def create_circle2_boundary(self):
        rad = int(self.rad2)
        x, y = np.mgrid[:self.length, :self.length]
        circle = (x-rad*(self.length/2/rad))**2 + (y-rad*(self.length/2/rad))**2
        donut = (circle < (rad**2) + rad+self.length/4) &\
                (circle > (rad**2) - rad-self.length/4)
        self.circle2 = donut
        self.create_value_grid()

    def create_value_grid(self):
        circle1_vals = self.circle1
        circle2_vals = self.circle2
        temp_grid = np.zeros((self.length, self.length))
        temp_grid2 = np.zeros((self.length, self.length))
        for i in range(0, self.length):
            for j in range(0, self.length):
                if circle1_vals[i][j]:
                    temp_grid[i][j] = int(self.init_guess)

        for i in range(0, self.length):
            for j in range(0, self.length):
                if circle2_vals[i][j]:
                    temp_grid2[i][j] = 1

        self.valgrid = np.add(temp_grid, temp_grid2)
        self.boundary_compiler()

    def boundary_compiler(self):
        self.gg = np.add(self.circle1, self.circle2)
        self.finite_diff_method()

    def finite_diff_method(self):
        T = self.gg
        T2 = self.valgrid
        for iter in range(0, int(self.iterations)):
            for i in range(1, self.length - 1, int(self.delta)):
                for j in range(1, self.length - 1, int(self.delta)):
                    if not T[i, j]:
                        T2[i, j] = 0.25 * (T2[i + 1][j] + T2[i - 1][j] + T2[i][j + 1] + T2[i][j - 1])
                    else:
                        pass

        self.T = T2
        self.plotter()

    def plotter(self):
        plt.title("Potential plot for coaxial cylinders")
        plt.imshow(self.T)
        plt.show()
        self.iterlabel.pack_forget()


def main():
    root = Tk()
    root.title("Laplace Numerical Solver")
    root.geometry('800x450')
    root['bg'] = '#ffffff'
    App(root, 0)
    root.mainloop()


if __name__ == '__main__':
    main()

