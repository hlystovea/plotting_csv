import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from plot import main

root = tk.Tk()
root.title('Построить графики испытаний СВ')
root.geometry('394x32')
root.resizable(False, False)


is_bar = tk.BooleanVar(root)
is_bar_input = tk.Checkbutton(root, variable=is_bar, text='Сеть')
is_bar_input.grid(row=1, column=5)

width = tk.IntVar(root, value=8)
width_label = tk.Label(root, text='Ширина:')
width_label.grid(row=1, column=1)
width_input = tk.Spinbox(
    root, from_=1, to=48, increment=1, width=2, textvariable=width)
width_input.grid(row=1, column=2)

height = tk.IntVar(root, value=4)
height_label = tk.Label(root, text='Высота:')
height_label.grid(row=1, column=3)
height_input = tk.Spinbox(
    root, from_=1, to=48, increment=1, width=2, textvariable=height)
height_input.grid(row=1, column=4)

def on_submit_open():
    test_type = 'bar' if is_bar.get() else 'idling'
    width = int(width_input.get())
    height = int(height_input.get())

    files = fd.askopenfilenames(
        title='Выбрать csv-файлами',
        initialdir='/',
        filetypes=(('csv files', '*.csv'), ),
        )
    if files:
        saved_count = main(files, width, height, test_type)
        showinfo(
            title='Выполнено',
            message=f'Сохранено {saved_count} файлов'
        )


open_button = tk.Button(root, text='Выбрать файлы', command=on_submit_open)
open_button.grid(row=1, column=6)

root.mainloop()
