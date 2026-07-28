import tkinter as tk
from pathlib import Path

from custom_typing_.custom_typing import Settings, SettingsVar

from .widgets import (first_row, folder_name, save_button, tk_checkbutton,
                      tk_labels, tk_spinbox, window_settings)


def open_settings(
        root_window: tk.Tk,
        settings: Settings,
        strings: tuple,
        widgets_main: dict
):
    window = window_settings(root_window, 'Settings', '300x300+550+220', 3, 8)
    tk_labels(window, strings, 0, 5)
    widgets = SettingsVar(
        base_dir=first_row(window, 1, 0, str(settings['base_dir'])),
        original=folder_name(window, 1, 1, settings['original']),
        editor=folder_name(window, 1, 2, settings['editor']),
        translate=folder_name(window, 1, 3, settings['translate']),
        other_folder=folder_name(
            window, 1, 4, ', '.join(settings['other_folder'])
        ),
        delete=tk_checkbutton(window, 1, 5, settings['delete']),
        length_number=tk_spinbox(window, 1, 6, settings['length_number'])
    )
    # widgets: SettingsVar = {
    #     'base_dir': first_row(window, 1, 0, str(settings['base_dir'])),
    #     'original': folder_name(window, 1, 1, settings['original']),
    #     'editor': folder_name(window, 1, 2, settings['editor']),
    #     'translate': folder_name(window, 1, 3, settings['translate']),
    #     'other_folder': folder_name(
    #         window, 1, 4, ', '.join(settings['other_folder'])
    #     ),
    #     'delete': tk_checkbutton(window, 1, 5, settings['delete']),
    #     'length_number': tk_spinbox(window, 1, 6, settings['length_number'])
    # }
    save_button(
         window=window,
         column=0, row=7,
         settings=settings, widgets=widgets,
    )
