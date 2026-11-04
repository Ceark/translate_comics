import tkinter as tk
from pathlib import Path
from typing import TypedDict

# from tkinter import ttk


class MoveImagesSettings(TypedDict):
    where: str
    to: str
    suffix: str


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
    ignore_folder: list[str]
    delete: bool
    length_number: int
    move_images: MoveImagesSettings


class MoveImagesSettingsVar(TypedDict):
    where: tk.StringVar
    to: tk.StringVar
    suffix: tk.StringVar


class SettingsVar(TypedDict):
    """
    Переменные Var для виджетов окна настроек.
    """
    base_dir: tk.StringVar
    original: tk.StringVar
    editor: tk.StringVar
    translate: tk.StringVar
    other_folder: tk.StringVar
    ignore_folder: tk.StringVar
    delete: tk.BooleanVar
    length_number: tk.IntVar
    move_images: MoveImagesSettingsVar


class WidgetsMain(TypedDict):
    """
    Виджеты главного окна.
    """
    row_combobox: ttk.Combobox


class DictVariable(TypedDict):
    """
    Переменные Var для виджетов главного окна.
    """
    comic: tk.StringVar
    regime: tk.StringVar
    quantity: tk.IntVar
    where_from: tk.StringVar
    where_to: tk.StringVar
    suffix: tk.StringVar
    folders: tk.StringVar


class SiteSelectors(TypedDict):
    name_site: str
    selectors: list[str]
    tag: str
    symbol: str
