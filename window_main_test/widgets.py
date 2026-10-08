import tkinter as tk
from tkinter import ttk


def tk_window(title: str, geometry: str):
    """Создание главного окна."""
    window = tk.Tk()
    window.title(title)
    window.geometry(geometry)
    return window


def tk_frame(root: tk.Tk):
    """Создание фрэйма."""
    frame = ttk.Frame(root, padding=(3, 3, 12, 12))
    frame.grid(column=0, row=0, sticky=('nwes'))
    return frame


def configure(obj: tk.Tk | ttk.Frame, column: int = 0, row: int = 0):
    """Конфигурация."""
    for index in range(column):
        obj.columnconfigure(index, weight=1)
    for index in range(row):
        obj.rowconfigure(index, weight=1)
