from typing import Callable, List
from .Constants import (
    MONTH_EN, MONTH_SHORT_EN, MONTH_NP, MONTH_SHORT_NP,
    NUMBER_NP, WEEK_EN, WEEK_SHORT_EN, WEEK_NP, WEEK_SHORT_NP
)

# Type alias for a date formatter function
DateFormatter = Callable[["NepaliDate"], str]


def pad(n: int) -> str:
    """Pads a number with a leading zero if it's less than 10."""
    return f"{n:02d}" if n < 10 else str(n)


def np_digit(s: str) -> str:
    """Converts a string of digits to Nepali digits."""
    return ''.join(NUMBER_NP[ord(c) - 48] for c in s)

# Year formatters


def year_en(size: int) -> DateFormatter:
    from NepaliDate import NepaliDate

    def f(date: "NepaliDate") -> str:
        y = str(date.year)
        if size <= 2:
            return y[-2:]
        if size == 3:
            return y[-3:]
        return y
    return f


def year_np(size: int) -> DateFormatter:
    from NepaliDate import NepaliDate

    def f(date: "NepaliDate") -> str:
        y = str(date.year)
        if size <= 2:
            return np_digit(y[-2:])
        if size == 3:
            return np_digit(y[-3:])
        return np_digit(y)
    return f

# Month formatters


def month_en(size: int) -> DateFormatter:
    from NepaliDate import NepaliDate

    def f(date: "NepaliDate") -> str:
        m = date.month
        if size == 1:
            return str(m + 1)
        if size == 2:
            return pad(m + 1)
        if size == 3:
            return MONTH_SHORT_EN[m]
        return MONTH_EN[m]
    return f


def month_np(size: int) -> DateFormatter:
    from NepaliDate import NepaliDate

    def f(date: "NepaliDate") -> str:
        m = date.month
        if size == 1:
            return np_digit(str(m + 1))
        if size == 2:
            return np_digit(pad(m + 1))
        if size == 3:
            return MONTH_SHORT_NP[m]
        return MONTH_NP[m]
    return f

# Date/Week formatters


def date_en(size: int) -> DateFormatter:
    from NepaliDate import NepaliDate

    def f(date: "NepaliDate") -> str:
        d = date.day
        if size == 1:
            return str(d)
        if size == 2:
            return pad(d)
        if size == 3:
            return WEEK_SHORT_EN[date.weekday()]
        return WEEK_EN[date.weekday()]
    return f


def date_np(size: int) -> DateFormatter:
    from NepaliDate import NepaliDate

    def f(date: "NepaliDate") -> str:
        d = date.day
        if size == 1:
            return np_digit(str(d))
        if size == 2:
            return np_digit(pad(d))
        if size == 3:
            return WEEK_SHORT_NP[date.weekday()]
        return WEEK_NP[date.weekday()]
    return f


# Fixed string formatter
def pass_str(seq: str) -> DateFormatter:
    return lambda date: seq


# Map format characters to functions
fn = {
    'Y': year_en,
    'y': year_np,
    'M': month_en,
    'm': month_np,
    'D': date_en,
    'd': date_np,
}


def is_special(ch: str) -> bool:
    return ch in fn


def tokenize(format_str: str) -> List[DateFormatter]:
    in_quote = False
    seq = ""
    special = ""
    special_size = 0
    tokens: List[DateFormatter] = []

    for ch in format_str:
        if ch == special:
            special_size += 1
            continue

        if special:
            tokens.append(fn[special](special_size))
            special = ""
            special_size = 0

        if ch == '"':
            in_quote = not in_quote
            continue

        if not is_special(ch) or in_quote:
            seq += ch
        else:
            if seq:
                tokens.append(pass_str(seq))
                seq = ""
            special = ch
            special_size = 1

    if seq:
        tokens.append(pass_str(seq))
    elif special:
        tokens.append(fn[special](special_size))

    return tokens


def format_date(nepali_date: "NepaliDate", format_str: str) -> str:
    return ''.join(f(nepali_date) for f in tokenize(format_str))
