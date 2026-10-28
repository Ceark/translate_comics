import re


def check_num(newval):
    """Валидация введенного в поле числа."""
    return re.match('^[0-9]*$', newval) is not None and len(newval) <= 5


def check_suffix(newval):
    """Валидация введенного в поле суффикса."""
    return re.match(r'^\*\..*$', newval) is not None
