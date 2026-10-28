from pathlib import Path
from tkinter.ttk import Combobox

from win32com.client import Dispatch

from custom.klass import Comic


def shortcut(shortcut_path: str, target_path: str):
    """
    Функция создания ярлыка, Windows.

    - shortcut_path - адрес ярлыка;
    - target_path - файл, для которого создаётся ярлык;
    """
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.save()


def list_comics_combobox_update(combobox: Combobox, base_dir: Path):
    """Функиця для обновления 'values' Combobox - наполнится комиксами из
    папки base_dir."""
    combobox.configure(
        values=[
            value.name
            for value
            in base_dir.iterdir()
            if Comic(value).is_comic()
        ]
    )
