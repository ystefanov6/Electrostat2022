import numpy as np
from tkinter import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (
            FigureCanvasTkAgg)
from matplotlib.figure import Figure
from PIL import Image


class Rect:
    def __init__(self, length, x, y, x_off, y_off, radio):
        self.length = length
        self.radio = radio
        self.x, self.y, x_off, y_off = x, y, x_off, y_off
        grid = np.zeros((self.length, self.length), dtype=bool)

        if self.radio == 'S':
            grid[y_off:y + y_off, x_off:x + x_off] = True

        elif self.radio == 'H':
            grid[y_off:y + y_off, x_off] = True
            grid[y_off, x_off:x + x_off] = True
            grid[y_off:y + y_off, x + x_off - 1] = True
            grid[y + y_off - 1, x_off:x + x_off] = True

        self.rect = grid


class Circle:
    def __init__(self, length, rad, radio, xoffset, yoffset):
        self.rad = rad
        self.length = length
        self.radio = radio
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.adjusted_x_offset = self.xoffset-self.rad
        self.adusted_y_offset = self.yoffset-self.rad
        x, y = np.mgrid[:self.length, :self.length]
        circle = (x - self.rad - self.yoffset) ** 2 + \
                 (y - self.rad - self.xoffset) ** 2

        if self.radio == 'H':
            self.donut = (circle < self.rad ** 2 + self.rad + self.length / 4) & \
                         (circle > self.rad ** 2 - self.rad - self.length / 4)

        elif self.radio == 'S':
            self.donut = (circle < rad ** 2 + rad + length / 4)
        # print(len(self.donut))


class App:
    def __init__(self, parent):
        # self.radEntry = None
        self.parent = parent
        '''This class configures and populates the toplevel window.
                   top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        parent.geometry("660x480+389+107")
        parent.minsize(120, 1)
        parent.maxsize(1540, 845)
        parent.resizable(1, 1)
        parent.title("Laplace Numerical Solver")
        parent.configure(background="#fafaff")

        self.menubar = Menu(self.parent, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        self.parent.configure(menu=self.menubar)

        self.canvas = Canvas(parent)
        self.canvas.place(relx=0.017, rely=0.479, relheight=0.508
                           , relwidth=0.404)
        self.canvas.configure(background="#e4d9ff")
        self.canvas.configure(borderwidth="2")
        self.canvas.configure(insertbackground="black")
        self.canvas.configure(relief="ridge")
        self.canvas.configure(selectbackground="blue")
        self.canvas.configure(selectforeground="white")

        self.canvas2 = Canvas(parent)
        self.canvas2.place(relx=0.433, rely=0.294, relheight=0.694
                           , relwidth=0.554)
        self.canvas2.configure(background="#e4d9ff")
        self.canvas2.configure(borderwidth="2")
        self.canvas2.configure(insertbackground="#e4d9ff")
        self.canvas2.configure(relief="ridge")
        self.canvas2.configure(selectbackground="blue")
        self.canvas2.configure(selectforeground="white")

        self.delta = None
        self.length = None
        self.rads = []
        self.radValEntries = []
        self.circle_y_offsets = []
        self.circle_x_offsets = []
        self.iterations = None
        self.circles = []
        self.widths = []
        self.heights = []
        self.y_offsets = []
        self.x_offsets = []
        self.rectValEntries = []
        self.gg = None
        self.valgrids = []
        self.valgrid_comp = None
        self.T = None
        self.rectangles = []
        self.circleradio = None
        self.rectradio = None


        self.Label1 = Label(self.parent)
        self.Label1.place(relx=0.017, rely=0.042, height=21, width=104)
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#fafaff")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font="-family {Poppins} -size 9")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Delta (default=1):''')

        self.entry = Entry(self.parent)
        self.entry.place(relx=0.216, rely=0.042, height=20, relwidth=0.19)
        self.entry.configure(background="white")
        self.entry.configure(disabledforeground="#a3a3a3")
        self.entry.configure(font="-family {Poppins} -size 9")
        self.entry.configure(foreground="#000000")
        self.entry.configure(insertbackground="black")

        self.Label2 = Label(self.parent)
        self.Label2.place(relx=0.017, rely=0.104, height=21, width=74)
        self.Label2.configure(anchor='w')
        self.Label2.configure(background="#fafaff")
        self.Label2.configure(compound='left')
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Poppins} -size 9")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Size of Grid:''')

        self.entry2 = Entry(self.parent)
        self.entry2.place(relx=0.166, rely=0.104, height=20, relwidth=0.24)
        self.entry2.configure(background="white")
        self.entry2.configure(disabledforeground="#a3a3a3")
        self.entry2.configure(font="-family {Poppins} -size 9")
        self.entry2.configure(foreground="#000000")
        self.entry2.configure(insertbackground="black")

        self.Label3 = Label(self.parent)
        self.Label3.place(relx=0.116, rely=0.167, height=21, width=114)
        self.Label3.configure(anchor='w')
        self.Label3.configure(background="#fafaff")
        self.Label3.configure(compound='left')
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font="-family {Poppins ExtraBold} -size 9 -weight bold")
        self.Label3.configure(foreground="#30343f")
        self.Label3.configure(text='''Generate Shapes''')

        self.Button1 = Button(self.parent, command=self.open_popup_1)
        self.Button1.place(relx=0.017, rely=0.229, height=34, width=117)
        self.Button1.configure(activebackground="#273469")
        self.Button1.configure(activeforeground="white")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#273469")
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font="-family {Poppins} -size 9")
        self.Button1.configure(foreground="#ffffff")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="#ffffff")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Circle''')

        self.Button2 = Button(self.parent, command=self.open_popup_2)
        self.Button2.place(relx=0.216, rely=0.229, height=34, width=117)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#273469")
        self.Button2.configure(compound='left')
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font="-family {Poppins} -size 9")
        self.Button2.configure(foreground="#ffffff")
        self.Button2.configure(highlightbackground="#ffffff")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Rectangle''')

        self.Button3 = Button(self.parent, command=self.combine_func(self.temp_bound_comp, self.draw_boundaries))
        self.Button3.place(relx=0.017, rely=0.333, height=54, width=250)
        self.Button3.configure(activebackground="#ececec")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#1e2749")
        self.Button3.configure(compound='left')
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(font="-family {Poppins} -size 9 -weight bold")
        self.Button3.configure(foreground="#fafaff")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''Draw Boundaries''')

        self.Label4 = Label(self.parent)
        self.Label4.place(relx=0.433, rely=0.042, height=21, width=164)
        self.Label4.configure(anchor='w')
        self.Label4.configure(background="#fafaff")
        self.Label4.configure(compound='left')
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(font="-family {Poppins} -size 9")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''Input number of iterations:''')

        self.Button4 = Button(self.parent, command=self.use_entry)
        self.Button4.place(relx=0.499, rely=0.125, height=44, width=97)
        self.Button4.configure(activebackground="#ececec")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="#1e2749")
        self.Button4.configure(compound='left')
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(font="-family {Poppins} -size 9 -weight bold")
        self.Button4.configure(foreground="#ffffff")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(text='''Compute''')

        self.Button5 = Button(self.parent, command=self.save_plot)
        self.Button5.place(relx=0.732, rely=0.125, height=44, width=97)
        self.Button5.configure(activebackground="#ececec")
        self.Button5.configure(activeforeground="#000000")
        self.Button5.configure(background="#1e2749")
        self.Button5.configure(compound='left')
        self.Button5.configure(disabledforeground="#a3a3a3")
        self.Button5.configure(font="-family {Poppins} -size 9 -weight bold")
        self.Button5.configure(foreground="#ffffff")
        self.Button5.configure(highlightbackground="#ffffff")
        self.Button5.configure(highlightcolor="black")
        self.Button5.configure(pady="0")
        self.Button5.configure(text='''Save Plot...''')

        self.entry8 = Entry(self.parent)
        self.entry8.place(relx=0.732, rely=0.042, height=20, relwidth=0.24)
        self.entry8.configure(background="white")
        self.entry8.configure(disabledforeground="#a3a3a3")
        self.entry8.configure(font="-family {Poppins} -size 9")
        self.entry8.configure(foreground="#000000")
        self.entry8.configure(insertbackground="black")

    def use_entry(self):
        contents = self.entry.get()
        if contents != '':
            self.delta = contents
        else:
            self.delta = 1

        self.length = int(self.entry2.get())

        self.iterations = int(self.entry8.get())

        self.iterlabel = Label(self.parent)
        self.iterlabel.place(relx=0.616, rely=0.25, height=21, width=115)
        self.iterlabel.configure(anchor='w')
        self.iterlabel.configure(background="#fafaff")
        self.iterlabel.configure(compound='left')
        self.iterlabel.configure(disabledforeground="#a3a3a3")
        self.iterlabel.configure(font="-family {Poppins Light} -size 7")
        self.iterlabel.configure(foreground="#000000")
        self.iterlabel.configure(text=f'Computing for {self.iterations} iter...')

        self.create_circle_boundary()

    def create_circle_boundary(self):
        for rad, x_off, y_off in zip(self.rads, self.circle_x_offsets, self.circle_y_offsets):
            circle = Circle(self.length, rad, self.circleradio, x_off, y_off).donut
            self.circles.append(circle)

        self.create_rect_boundary()

    def create_rect_boundary(self):
        for width, height, x_off, y_off in zip(self.widths, self.heights, self.x_offsets, self.y_offsets):
            rectangle = Rect(self.length, width, height, x_off, y_off, self.rectradio).rect
            self.rectangles.append(rectangle)
        # print(len(self.rectangles))
        self.create_value_grid()

    def create_value_grid(self):
        for circle, values in zip(self.circles, self.radValEntries):
            temp_grid = np.zeros((self.length, self.length))
            for i in range(0, self.length):
                for j in range(0, self.length):
                    if circle[i][j]:
                        temp_grid[i][j] = values

            self.valgrids.append(temp_grid)

        for rectangle, rect_values in zip(self.rectangles, self.rectValEntries):
            temp_grid2 = np.zeros((self.length, self.length))
            for i in range(0, self.length):
                for j in range(0, self.length):
                    if rectangle[i][j]:
                        temp_grid2[i][j] = rect_values
            self.valgrids.append(temp_grid2)

        self.value_compiler()

    def value_compiler(self):
        self.valgrid_comp = sum(self.valgrids)
        self.boundary_compiler()

    def boundary_compiler(self):
        self.boundary_combo = self.circles + self.rectangles
        self.gg = sum(self.boundary_combo)
        self.finite_diff_method()

    def finite_diff_method(self):
        T = self.gg
        T2 = self.valgrid_comp
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
        self.fig2 = Figure(figsize=(5, 5), dpi=100)

        heatmap = self.fig2.add_subplot(111).imshow(self.T)
        self.fig2.colorbar(heatmap)


        try:
            self.canvas2.destroy()
        except Exception:
            pass
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.parent)  # A tk.DrawingArea.
        self.canvas2.get_tk_widget().place(relx=0.433, rely=0.294, relheight=0.694
                , relwidth=0.554)
        self.canvas2.get_tk_widget().configure(background="#e4d9ff")
        self.canvas2.get_tk_widget().configure(borderwidth="2")
        self.canvas2.get_tk_widget().configure(insertbackground="black")
        self.canvas2.get_tk_widget().configure(relief="ridge")
        self.canvas2.get_tk_widget().configure(selectbackground="blue")
        self.canvas2.get_tk_widget().configure(selectforeground="white")
        self.canvas2.flush_events()

    def open_popup_1(self):
        top3 = Toplevel(self.parent)
        top3.geometry("400x400")
        top3.title("Input Data")
        top3.configure(background="#fafaff")
        self.Label10 = Label(top3)
        self.Label10.pack()
        self.Label10.configure(anchor='w')
        self.Label10.configure(background="#fafaff")
        self.Label10.configure(compound='left')
        self.Label10.configure(disabledforeground="#a3a3a3")
        self.Label10.configure(font="-family {Poppins} -size 9")
        self.Label10.configure(foreground="#000000")
        self.Label10.configure(text='''Input radius''')

        self.radEntry = Entry(top3)
        self.radEntry.pack()
        self.radEntry.configure(background="white")
        self.radEntry.configure(disabledforeground="#a3a3a3")
        self.radEntry.configure(font="TkFixedFont")
        self.radEntry.configure(foreground="#000000")
        self.radEntry.configure(insertbackground="black")

        self.Label11 = Label(top3)
        self.Label11.pack()
        self.Label11.configure(anchor='w')
        self.Label11.configure(background="#fafaff")
        self.Label11.configure(compound='left')
        self.Label11.configure(disabledforeground="#a3a3a3")
        self.Label11.configure(font="-family {Poppins} -size 9")
        self.Label11.configure(foreground="#000000")
        self.Label11.configure(text='''Input value at boundary''')

        self.valEntry = Entry(top3)
        self.valEntry.pack()
        self.valEntry.configure(background="white")
        self.valEntry.configure(disabledforeground="#a3a3a3")
        self.valEntry.configure(font="TkFixedFont")
        self.valEntry.configure(foreground="#000000")
        self.valEntry.configure(insertbackground="black")

        self.Label12 = Label(top3)
        self.Label12.pack()
        self.Label12.configure(anchor='w')
        self.Label12.configure(background="#fafaff")
        self.Label12.configure(compound='left')
        self.Label12.configure(disabledforeground="#a3a3a3")
        self.Label12.configure(font="-family {Poppins} -size 9")
        self.Label12.configure(foreground="#000000")
        self.Label12.configure(text='''Input x-offset (to center: grid size / 2)''')

        self.circle_x_off = Entry(top3)
        self.circle_x_off.pack()
        self.circle_x_off.configure(background="white")
        self.circle_x_off.configure(disabledforeground="#a3a3a3")
        self.circle_x_off.configure(font="TkFixedFont")
        self.circle_x_off.configure(foreground="#000000")
        self.circle_x_off.configure(insertbackground="black")

        self.Label13 = Label(top3)
        self.Label13.pack()
        self.Label13.configure(anchor='w')
        self.Label13.configure(background="#fafaff")
        self.Label13.configure(compound='left')
        self.Label13.configure(disabledforeground="#a3a3a3")
        self.Label13.configure(font="-family {Poppins} -size 9")
        self.Label13.configure(foreground="#000000")
        self.Label13.configure(text='''Input y-offset (to center: grid size / 2)''')

        self.circle_y_off = Entry(top3)
        self.circle_y_off.pack()
        self.circle_y_off.configure(background="white")
        self.circle_y_off.configure(disabledforeground="#a3a3a3")
        self.circle_y_off.configure(font="TkFixedFont")
        self.circle_y_off.configure(foreground="#000000")
        self.circle_y_off.configure(insertbackground="black")

        self.circlevar = IntVar()
        Radiobutton(top3, text="Hollow", variable=self.circlevar, value=1, command=self.circle_radio).pack()
        Radiobutton(top3, text="Solid", variable=self.circlevar, value=2, command=self.circle_radio).pack()

        self.Button11 = Button(top3, command=self.combine_func(self.get_rads, top3.destroy))
        self.Button11.pack(pady=5)
        self.Button11.configure(activebackground="#273469")
        self.Button11.configure(activeforeground="white")
        self.Button11.configure(activeforeground="#000000")
        self.Button11.configure(background="#273469")
        self.Button11.configure(compound='left')
        self.Button11.configure(disabledforeground="#a3a3a3")
        self.Button11.configure(font="-family {Poppins} -size 9")
        self.Button11.configure(foreground="#ffffff")
        self.Button11.configure(highlightbackground="#d9d9d9")
        self.Button11.configure(highlightcolor="#ffffff")
        self.Button11.configure(pady="0")
        self.Button11.configure(text='''Confirm''')

    def get_rads(self):
        self.rads.append(int(self.radEntry.get()))
        #print(len(self.rads))
        self.radValEntries.append(int(self.valEntry.get()))
        self.circle_x_offsets.append(int(self.circle_x_off.get()))
        self.circle_y_offsets.append(int(self.circle_y_off.get()))

    def open_popup_2(self):
        top2 = Toplevel(self.parent)
        top2.geometry("400x400")
        top2.title("Input Data")
        top2.configure(background="#fafaff")
        self.Label5 = Label(top2)
        self.Label5.pack()
        self.Label5.configure(anchor='w')
        self.Label5.configure(background="#fafaff")
        self.Label5.configure(compound='left')
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(font="-family {Poppins} -size 9")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(text='''Input height''')

        self.heightEntry = Entry(top2)
        self.heightEntry.pack()
        self.heightEntry.configure(background="white")
        self.heightEntry.configure(disabledforeground="#a3a3a3")
        self.heightEntry.configure(font="TkFixedFont")
        self.heightEntry.configure(foreground="#000000")
        self.heightEntry.configure(insertbackground="black")

        self.Label6 = Label(top2)
        self.Label6.pack()
        self.Label6.configure(anchor='w')
        self.Label6.configure(background="#fafaff")
        self.Label6.configure(compound='left')
        self.Label6.configure(disabledforeground="#a3a3a3")
        self.Label6.configure(font="-family {Poppins} -size 9")
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(text='''Input width''')

        self.widthEntry = Entry(top2)
        self.widthEntry.pack()
        self.widthEntry.configure(background="white")
        self.widthEntry.configure(disabledforeground="#a3a3a3")
        self.widthEntry.configure(font="TkFixedFont")
        self.widthEntry.configure(foreground="#000000")
        self.widthEntry.configure(insertbackground="black")

        self.Label7 = Label(top2)
        self.Label7.pack()
        self.Label7.configure(anchor='w')
        self.Label7.configure(background="#fafaff")
        self.Label7.configure(compound='left')
        self.Label7.configure(disabledforeground="#a3a3a3")
        self.Label7.configure(font="-family {Poppins} -size 9")
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(text='''Input x-offset''')

        self.xOffsetEntry = Entry(top2)
        self.xOffsetEntry.pack()
        self.xOffsetEntry.configure(background="white")
        self.xOffsetEntry.configure(disabledforeground="#a3a3a3")
        self.xOffsetEntry.configure(font="TkFixedFont")
        self.xOffsetEntry.configure(foreground="#000000")
        self.xOffsetEntry.configure(insertbackground="black")

        self.Label8 = Label(top2)
        self.Label8.pack()
        self.Label8.configure(anchor='w')
        self.Label8.configure(background="#fafaff")
        self.Label8.configure(compound='left')
        self.Label8.configure(disabledforeground="#a3a3a3")
        self.Label8.configure(font="-family {Poppins} -size 9")
        self.Label8.configure(foreground="#000000")
        self.Label8.configure(text='''Input y-offset''')

        self.yOffsetEntry = Entry(top2)
        self.yOffsetEntry.pack()
        self.yOffsetEntry.configure(background="white")
        self.yOffsetEntry.configure(disabledforeground="#a3a3a3")
        self.yOffsetEntry.configure(font="TkFixedFont")
        self.yOffsetEntry.configure(foreground="#000000")
        self.yOffsetEntry.configure(insertbackground="black")

        self.Label9 = Label(top2)
        self.Label9.pack()
        self.Label9.configure(anchor='w')
        self.Label9.configure(background="#fafaff")
        self.Label9.configure(compound='left')
        self.Label9.configure(disabledforeground="#a3a3a3")
        self.Label9.configure(font="-family {Poppins} -size 9")
        self.Label9.configure(foreground="#000000")
        self.Label9.configure(text='''Input value at boundary''')

        self.rectVals = Entry(top2)
        self.rectVals.pack()
        self.rectVals.configure(background="white")
        self.rectVals.configure(disabledforeground="#a3a3a3")
        self.rectVals.configure(font="TkFixedFont")
        self.rectVals.configure(foreground="#000000")
        self.rectVals.configure(insertbackground="black")

        self.rectvar = IntVar()
        Radiobutton(top2, text="Hollow", variable=self.rectvar, value=1, command=self.rectangle_radio).pack()
        Radiobutton(top2, text="Solid", variable=self.rectvar, value=2, command=self.rectangle_radio).pack()

        self.Button10 = Button(top2, command=self.combine_func(self.get_rect_data, top2.destroy))
        self.Button10.pack(pady=5)
        self.Button10.configure(activebackground="#273469")
        self.Button10.configure(activeforeground="white")
        self.Button10.configure(activeforeground="#000000")
        self.Button10.configure(background="#273469")
        self.Button10.configure(compound='left')
        self.Button10.configure(disabledforeground="#a3a3a3")
        self.Button10.configure(font="-family {Poppins} -size 9")
        self.Button10.configure(foreground="#ffffff")
        self.Button10.configure(highlightbackground="#d9d9d9")
        self.Button10.configure(highlightcolor="#ffffff")
        self.Button10.configure(pady="0")
        self.Button10.configure(text='''Confirm''')

    def get_rect_data(self):
        self.heights.append(int(self.heightEntry.get()))
        self.widths.append(int(self.widthEntry.get()))
        self.x_offsets.append(int(self.xOffsetEntry.get()))
        self.y_offsets.append(int(self.yOffsetEntry.get()))
        self.rectValEntries.append(int(self.rectVals.get()))

    def combine_func(self, *funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)

        return combined_func

    def draw_boundaries(self):

        fig = Figure(figsize=(4, 5), dpi=100)

        fig.add_subplot(111).imshow(self.gg, cmap='Greys',  interpolation='nearest')

        try:
            self.canvas.destroy()
        except Exception:
            pass
        self.canvas = FigureCanvasTkAgg(fig, master=self.parent)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().place(relx=0.017, rely=0.479, relheight=0.508
                           , relwidth=0.404)
        self.canvas.get_tk_widget().configure(background="#e4d9ff")
        self.canvas.get_tk_widget().configure(borderwidth="2")
        self.canvas.get_tk_widget().configure(insertbackground="black")
        self.canvas.get_tk_widget().configure(relief="ridge")
        self.canvas.get_tk_widget().configure(selectbackground="blue")
        self.canvas.get_tk_widget().configure(selectforeground="white")
        self.canvas.flush_events()

    def temp_bound_comp(self):
        self.length = int(self.entry2.get())
        print(self.length)
        self.circles = []
        self.rectangles = []
        for rad, x_off, y_off in zip(self.rads, self.circle_x_offsets, self.circle_y_offsets):
            circle = Circle(self.length, rad, self.circleradio, x_off, y_off).donut
            self.circles.append(circle)

        for width, height, x_off, y_off in zip(self.widths, self.heights, self.x_offsets, self.y_offsets):
            rectangle = Rect(self.length, width, height, x_off, y_off, self.rectradio).rect
            self.rectangles.append(rectangle)

        self.boundary_combo = self.circles + self.rectangles
        self.gg = sum(self.boundary_combo)
        print(self.gg)

    def save_plot(self):

        self.fig2.savefig('temp.png')

        image = Image.open("temp.png")
        dialogue = image.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(
            ('PNG', '*.png'), ('BMP', ('*.bmp', '*.jdib')), ('GIF', '*.gif')))
        image.save(dialogue)

    def circle_radio(self):
        choice = self.circlevar.get()
        if choice == 1:
            output = "H"

        elif choice == 2:
            output = "S"

        else:
            output = "Invalid selection"

        self.circleradio = output
        print(self.circleradio)

    def rectangle_radio(self):
        choice = self.rectvar.get()
        if choice == 1:
            output = "H"

        elif choice == 2:
            output = "S"

        else:
            output = "Invalid selection"

        self.rectradio = output
        print(self.rectradio)


def main():
    root = Tk()
    root.title("Laplace Numerical Solver")
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
