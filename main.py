import os

import pyinputplus as pyip
from dotenv import load_dotenv

import functions

load_dotenv()


def main():
    BASE_DIR = os.getenv('BASE_DIR', os.getcwd)
    os.chdir(BASE_DIR)
    dict_functions = {
        'Create comics': functions.create_comics,
        'Create new chapter': functions.create_new_chapter,
        'Extract image': functions.extract_image
    }
    while True:
        action = pyip.inputMenu(
            [key for key in dict_functions.keys()],
            numbered=True,
            prompt='Выберете команду:\n'
        )
        answer = dict_functions[action]()
        print(answer)


if __name__ == '__main__':
    main()
