from pathlib import Path


class Chapter(Path):
    """
    Глава комикса.
    """
    technical_folder: list[str] = []

    @classmethod
    def update_technical_folder(self, new_folders: list[str]):
        self.technical_folder = new_folders.copy()

    @property
    def number(self):
        """Номер главы комикса."""
        string = ''
        for symbol in self.name:
            if symbol.isdecimal():
                string += symbol
            else:
                break
        return string

    def create(self):
        """
        Создать главу комикса со всеми техническими папками.
        """
        for folder in self.technical_folder:
            (self / folder).mkdir(parents=True, exist_ok=True)
