import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import TypedDict


class Settings(TypedDict):
    """
    Представление настроек в том виде,
    в котором они должны быть загружены из json-файла.
    """
    base_dir: Path
    original: str
    editor: str
    translate: str
    other_folder: list[str]
    delete: bool
    length_number: int


class WidgetsVar(TypedDict):
    base_dir: tk.StringVar
    original: tk.StringVar
    editor: tk.StringVar
    translate: tk.StringVar
    other_folder: tk.StringVar
    delete: tk.BooleanVar
    length_number: tk.IntVar


class WidgetsMain(TypedDict):
    row_combobox: ttk.Combobox
