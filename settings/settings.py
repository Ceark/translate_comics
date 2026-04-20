import tkinter as tk
from pathlib import Path

from dotenv import load_dotenv

from .extract_env import (additional_directories, base_dir, delete_file,
                          length_number, universal_directory)


def first_start(path_main_folder: Path):
    with open('.env', 'w', encoding='utf-8') as file:
        text_file = '\n\n'.join(
            (
                f'BASE_DIR = {path_main_folder}',
                'ORIGINAL = Original',
                'EDITOR = Editor',
                'TRANSLATE = Translate',
                'ADDITIONAL_FOLDERS = Text',
                'LENGTH_NUMBER = 2',
                'DELETE = False'
            )
        )
        file.write(text_file)


path_env = Path('.', '.env')
# if not load_dotenv(path_env):
if True:

    # Окно ввода
    pady = 5

    window = tk.Tk()
    window.title("translate_comics")
    window.geometry('400x100')

    label = tk.Label(
        window,
        text='Адрес папки для комиксов',
        font=('Arial', 14)
    )
    label.pack(pady=pady)

    entry = tk.Entry(
        window,
        font=('Arial', 14),
        width=30
    )
    entry.pack(pady=pady)

    def show_input():
        user_input = entry.get()
        first_start(Path(user_input))
        window.destroy()

    button = tk.Button(window, text='test', command=show_input)
    button.pack(pady=pady)

    window.mainloop()
    # Конец окна ввода

    load_dotenv()

BASE_DIR = base_dir()

ORIGINAL = universal_directory('ORIGINAL', 'Original')

EDITOR = universal_directory('EDITOR', 'Editor')

TRANSLATE = universal_directory('TRANSLATE', 'Translate')

NAMED_DIRS = (ORIGINAL, EDITOR, TRANSLATE)

ADDITIONAL = additional_directories(NAMED_DIRS)

LENGTH_NUMBER = length_number(1, 5)

DELETE = delete_file()
