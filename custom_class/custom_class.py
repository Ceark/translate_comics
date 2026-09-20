from pathlib import Path
import re


class Folder(Path):
    """Заготовка папки."""
    technical_folders: list[str] = []
    ignored_folders: list[str] = []

    def update_union(self, old_list: list[str], new_list: list[str]):
        """
        Заменить содежимое списка содержимым другого списка.

        Предполагается, что эта функция применяется для обновления содержимого
        self.technical_folders и self.ignored_folders.
        """
        old_list.clear()
        old_list.extend(new_list)

    @property
    def union_folders(self):
        """Список технических и игнорируемых папок."""
        return self.technical_folders + self.ignored_folders


class Chapter(Folder):
    """
    Глава комикса.
    """
    @property
    def number(self) -> int | float:
        """Номер главы комикса."""
        try:
            pattern = re.compile(r'\d+(?:\.\d+)?')
            number = pattern.match(self.name).group()
            return float(number) if '.' in number else int(number)
        except AttributeError:
            return 0

    def is_chapter(self) -> bool:
        if (
            self.name not in self.union_folders
            and self.name[0].isdecimal()
            and self.is_dir()
        ):
            return True
        return False


class Comic(Folder):
    """
    Комикс.
    """
    def is_comic(self) -> bool:
        if (
            self.name not in self.union_folders
            and self.is_dir()
        ):
            return True
        return False

    def list_chapters(self) -> list[Chapter]:
        """Список глав комикса."""
        chapters = [
            Chapter(chapter)
            for chapter
            in self.iterdir()
            if Chapter(chapter).is_chapter()
        ]
        return chapters

    def number_last_chapter(self) -> int:
        """Номер последней главы.

        Возвращает наибольший номер главы, преобразованный в int.
        Если глав нет, то возвращает 0."""
        number = max(self.list_chapters(), key=Chapter.number, default=0)
        if isinstance(number, int):
            return number
        return int(number.number)

    def create_chapters(self, quantity=1):
        """Создать подпапку, главу комикса."""
        new_chapter = self.number_last_chapter() + 1
        for number in range(new_chapter, new_chapter + quantity):
            for folder in self.technical_folders:
                (self / number / folder).mkdir(exist_ok=True, parents=True)
