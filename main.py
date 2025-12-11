from time import sleep

import pyinputplus as pyip

from custom_class import MainFolder
from extract_env import BASE_DIR


def main():
    if BASE_DIR:
        main_dir = MainFolder(BASE_DIR)
        dict_functions = {
            'Создать комикс': main_dir.create_comic,
            'Добавить часть': main_dir.add_chapter,
            'Извлечь изображения': main_dir.extract_image,
            'Переместить изображения': main_dir.move_images,
            'Создать ярлыки': main_dir.create_shortcut,
        }
        while True:
            action = pyip.inputMenu(
                [key for key in dict_functions.keys()],
                numbered=True,
                prompt='Выберите команду:\n',
                blank=True
            )
            if action:
                answer = dict_functions[action]()
                print(answer)
                print('------')
            else:
                break
    print('Завершение работы.')
    sleep(5)


if __name__ == '__main__':
    main()
