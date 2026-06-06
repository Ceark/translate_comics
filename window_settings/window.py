import json
from pathlib import Path
from tkinter import messagebox

from widget import (first_row, folder_name, save_button, tk_checkbutton,
                    tk_labels, tk_spinbox, tk_window)


def window_settings(strings_label):
    """
    Готовое окно настроек.
    """
    def create_data_widgets():
        return {
            'base_dir': first_row(window, 1, 0, settings['base_dir']),
            'original': folder_name(window, 1, 1, settings['original']),
            'editor': folder_name(window, 1, 2, settings['editor']),
            'translate': folder_name(window, 1, 3, settings['translate']),
            'other_folder': folder_name(window, 1, 4, settings['other_folder']),
            'delete': tk_checkbutton(window, 1, 5, settings['delete']),
            'length_number': tk_spinbox(window, 1, 6, settings['length_number'])
        }

    window = tk_window('Settings', 3, 8)
    tk_labels(window, strings_label, 0)
    default_settings = {
        'base_dir': str(Path('D://', 'Комиксы')),
        'original': 'Original',
        'editor': 'Редактор',
        'translate': 'Перевод',
        'other_folder': 'Текст',
        'delete': False,
        'length_number': 2
    }
    try:  # Если файл настроек не существует...
        with open('./settings.json', 'r', encoding='utf-8') as file:
            settings = json.load(file)
            settings['other_folder'] = ', '.join(settings['other_folder'])
    except (FileNotFoundError, KeyError):
        settings = default_settings
    try:  # Если в файле настроек нет нужных ключей...
        data_widgets = create_data_widgets()
    except KeyError:
        settings = default_settings
        data_widgets = create_data_widgets()
        messagebox.showinfo(
            title='Error',
            message='Используются настройки по умолчанию.'
        )
    save_button(window, 0, 7, data_widgets)
    window.mainloop()


if __name__ == '__main__':
    string_label = (
        'Комиксы',
        'Оригинал',
        'Редактор',
        'Перевод',
        'Доп. папки',
        'Удалить файлы',
        'Длина числа',
    )
    window_settings(string_label)
