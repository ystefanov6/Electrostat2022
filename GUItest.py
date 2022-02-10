from tkinter import *


class App:
    def __init__(self, parent):
        self.parent = parent
        self.label = Label(text=f'Delta value:')
        self.label.pack()
        self.entry = Entry(self.parent)
        self.entry.pack()
        self.button = Button(parent, text='OK', command=self.use_entry)
        self.button.pack()

    def use_entry(self):
        contents = self.entry.get()
        delta = contents
        print(contents)
        return contents



