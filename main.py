from pathlib import Path
from time import sleep

import pyinputplus as pyip

from custom_class import MainFolder
from extract_env import BASE_DIR


def main():
    if not (
        Path(BASE_DIR).is_absolute()
        and Path(BASE_DIR).exists()
    ):
        print('Неверный адрес BASE_DIR. Завершение работы.')
        sleep(5)
    main_dir = MainFolder(BASE_DIR)
    dict_functions = {
        'Create comics': main_dir.create_comic,
        'Add chapter': main_dir.add_chapter,
        'Extract image': main_dir.extract_image
    }
    while True:
        action = pyip.inputMenu(
            [key for key in dict_functions.keys()],
            numbered=True,
            prompt='Выберете команду:\n',
            blank=True
        )
        answer = dict_functions[action]()
        print(answer)


if __name__ == '__main__':
    main()
