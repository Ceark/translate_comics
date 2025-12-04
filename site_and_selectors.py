"""
ALL - словарь сочетаний функции-экстрактора и
параметров функции для каждого сайта.
"""

from pathlib import Path

import bs4


def extract_one(
    example_soup: bs4.BeautifulSoup,
    site_dir: Path,
    selectors: list[str],
    tag: str,
    symbol: str
):
    """
    Возвращает список имен файлов.
    """
    for selector in selectors:
        parts = example_soup.select(selector)
        if parts:
            for part in parts:
                elems: list[str] = [
                    str(child.attrs[tag]) for child
                    in part.children
                    if isinstance(child, bs4.element.Tag)
                ]
                elems = [
                    Path(value).name.partition(symbol)[0]
                    for value in elems
                ]
                validate = [
                    (site_dir / file).exists()
                    for file in elems
                ]
                if False not in validate:
                    return elems
        return []


tapas = [
    'article[class="viewer__body js-episode-article main__body"]',
    'article[class="viewer__body js-episode-article main__body '
    'hidden js-mature-content"]'
]
webtoons = [
    'div[class="viewer_img _img_viewer_area"]'
]


names_site = {
    'tapas': 'tapas',
    'webtoons': 'webtoons'
}

parameters = {
    names_site['tapas']: {
        'selectors': tapas,
        'tag': 'data-src',
        'symbol': '*'
    },
    names_site['webtoons']: {
        'selectors': webtoons,
        'tag': 'data-url',
        'symbol': '?'
    }
}

function = {
    names_site['tapas']: extract_one,
    names_site['webtoons']: extract_one
}

SETTINGS = {
    site: {
        'function': function[names_site[site]],
        'parameters': parameters[names_site[site]]
    }
    for site
    in names_site
}
