import json
from pathlib import Path

from widget import (first_row, folder_name, save_button, tk_checkbutton,
                    tk_labels, tk_spinbox, tk_window)


def window_settings():
    """
    Готовое окно настроек.
    """
    window = tk_window(3, 8)
    string_label = (
        'Комиксы',
        'Оригинал',
        'Редактор',
        'Перевод',
        'Доп. папки',
        'Удалить файлы',
        'Длина числа',
    )
    tk_labels(window, string_label, 0)

    try:
        with open('./settings.json', 'r', encoding='utf-8') as file:
            settings = json.load(file)
            settings['other_folder'] = ', '.join(settings['other_folder'])
    except FileNotFoundError:
        settings = {
            'base_dir': str(Path('D://', 'Комиксы')),
            'original': 'Original',
            'editor': 'Редактор',
            'translate': 'Перевод',
            'other_folder': ('Текст',),
            'delete': False,
            'length_number': 2
        }

    data_widgets = {
        'base_dir': first_row(window, 1, 0, settings['base_dir']),
        'original': folder_name(window, 1, 1, settings['original']),
        'editor': folder_name(window, 1, 2, settings['editor']),
        'translate': folder_name(window, 1, 3, settings['translate']),
        'other_folder': folder_name(window, 1, 4, settings['other_folder']),
        'delete': tk_checkbutton(window, 1, 5, settings['delete']),
        'length_number': tk_spinbox(window, 1, 6, settings['length_number'])
    }
    save_button(window, 0, 7, data_widgets)

    window.mainloop()


if __name__ == '__main__':
    window_settings()
