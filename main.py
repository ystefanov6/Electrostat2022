import matplotlib.pyplot as plt
import numpy as np
from tkinter import *


class Rect:
    def __init__(self, x, y, length):
        self.length = length
        grid = np.mgrid[:self.length, :self.length]
        grid[(length - 1):, :] = x
        grid[:1, :] = x
        grid[:, (length - 1):] = y
        grid[:, :1] = y

        self.rect = grid


class Circle:
    def __init__(self, length, rad):
        self.rad = rad
        self.length = length
        x, y = np.mgrid[:self.length, :self.length]
        circle = (x - self.rad * (self.length / 2 / self.rad)) ** 2 + \
                 (y - self.rad * (self.length / 2 / self.rad)) ** 2
        self.donut = (circle < self.rad ** 2 + self.rad + self.length / 4) & \
                     (circle > self.rad ** 2 - self.rad - self.length / 4)


class App:
    def __init__(self, parent):
        self.parent = parent

        self.delta = None
        self.length = None
        self.init_guess = None
        self.rad1 = None
        self.rad2 = None
        self.iterations = None
        self.circle1 = None
        self.circle2 = None
        self.gg = None
        self.valgrid = None
        self.T = None
        self.rect1 = None
        self.rect2 = None
        self.rect3 = None
        self.rect4 = None

        Label(text=f'Delta value: (default = 1)').pack()
        self.entry = Entry(self.parent).pack()

        Label(text="Length:").pack()
        self.entry2 = Entry(self.parent).pack()

        Label(text="Initial guess:").pack()
        self.entry3 = Entry(self.parent).pack()

        Label(text="BOUNDARY CONDITIONS").pack(fill='x', pady=20)
        Button(text="Create circle", command=self.open_popup).pack()

        Button(text="Compute", command=self.use_entry).pack()

        Label(text="Number of iterations:").pack()
        self.entry8 = Entry(self.parent).pack()

    def use_entry(self):
        contents = self.entry.get()
        if contents != '':
            self.delta = contents
        else:
            self.delta = 1

        self.length = int(self.entry2.get()) + 1

        self.init_guess = int(self.entry3.get())

        self.rad1 = int(self.entry4.get())

        self.rad2 = int(self.entry5.get())

        self.iterations = int(self.entry8.get())

        self.iterlabel = Label(self.parent, text=f"Computing for {self.iterations} iterations...", bg="#ffffff").pack()

        self.create_circle_boundary()

    def create_circle_boundary(self):
        Circle(self.length, self.rad1)
        self.create_value_grid()

    def create_rect_boundary(self):
        Rect(self.width, self.height, self.length)

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

    def open_popup(self):
        top = Toplevel(self.parent)
        top.geometry("400x400")
        top.title("Input Data")
        Label(top, text="Input Radius").pack()
        Entry(top).pack()
        Button(text="Confirm", command=)

    def get(self):
        return

def main():
    root = Tk()
    root.title("Laplace Numerical Solver")
    root.geometry('800x450')
    root['bg'] = '#ffffff'
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
