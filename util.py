from collections.abc import Iterable


def convert(s: str):
    """
    >>> convert("20")
    20
    >>> convert("hello")
    'hello'
    >>> convert("1-23")
    (1, 23)
    """
    if "-" in s:
        parts = s.split("-")
        if all(part.isdecimal() for part in parts):
            return tuple(map(int, parts))
    elif s.isdecimal():
        return int(s)
    else:
        return s


def display(obj):
    for attr, val in obj.__dict__.items():
        print(f"{attr} = {val}")
        if isinstance(val, Iterable) and not isinstance(val, str):
            for elem in val:
                try:
                    print(f"\t{elem.__dict__}")
                except AttributeError:
                    print(f"\t{elem}")

