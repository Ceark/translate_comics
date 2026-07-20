from functools import partial
from pathlib import Path

from custom_typing import PythonTwoSettings
from window_settings.window import open_settings

from .widgets import button_settings, row_combobox, tk_window


def open_main(
    settings: PythonTwoSettings,
    path_settings: Path
):
    window = tk_window('tr_comic', '200x320+500+190', 2, 4)
    base_dir = row_combobox(window, 0, 0, settings)

    strings = (
        'Комиксы',
        'Оригинал',
        'Редактор',
        'Перевод',
        'Доп. папки',
        'Удалить файлы',
        'Длина числа',
    )
    command_settings = partial(
        open_settings, window, path_settings, settings, strings
    )
    button_settings(
        window, 'Настройки', command_settings,
        column=1, row=3
    )
    window.mainloop()
