from pathlib import Path
from time import sleep

import pyinputplus as pyip

from custom_class import MainFolder
from extract_env import BASE_DIR


def main():
    if BASE_DIR:
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
            if action:
                answer = dict_functions[action]()
                print(answer)
            else:
                break
    print('Завершение работы.')
    sleep(5)


if __name__ == '__main__':
    main()
