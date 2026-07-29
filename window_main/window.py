import tkinter as tk
from pathlib import Path

from constants import strings
from custom_typing.custom_typing import Settings

from .widgets import button_settings, row_combobox, tk_window


def open_main(
    settings: Settings,
    path_settings: Path
):
    window = tk_window('tr_comic', '200x320+500+190', 2, 4)
    dif_var = {
        'row_combobox': tk.StringVar()
    }
    widgets_one = {
        'row_combobox': row_combobox(
            window=window, settings=settings,
            column=0, row=0,
            str_var=dif_var['row_combobox']
        ),
    }
    widgets_two = {
        'settings': button_settings(
            window=window, settings=settings,
            column=1, row=3,
            text='Настройки', strings=strings,
            widgets_main=widgets_one
        )
    }

    window.mainloop()
