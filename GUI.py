
from tkinter import *
ws = Tk()
ws.title("Laplace Numerical Solver")
ws.geometry('400x300')
ws['bg'] = '#ffffff'


def send_input():
    delta = player_name.get()
    Label(ws, text=f'Delta value: {delta}').pack()
    print(delta)
    return delta


player_name = Entry(ws)
player_name.pack(pady=30)

Button(
    ws,
    text="Enter delta:",
    padx=10,
    pady=5,
    command=send_input
    ).pack()

ws.mainloop()

