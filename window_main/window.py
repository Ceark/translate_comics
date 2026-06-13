import json
from pathlib import Path

from widget import (field_create_chapters, field_create_comic, row_combobox,
                    tk_window, field_settings, extract_image)

if __name__ == '__main__':
    window = tk_window('tr_comics', 2, 4)
    widget = {
        'combobox': row_combobox(window, 0, 0, Path('D://')),
        'create_comic': field_create_comic(window, 1, 1),
        'add_chapter': field_create_chapters(window, 1, 2),
        'setting': field_settings(window, 1, 3),
        'extract_image': extract_image(window, 0, 1),
    }
    window.mainloop()
