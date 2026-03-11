from typing import Callable, List
from .Constants import (
    MONTH_EN, MONTH_SHORT_EN, MONTH_NP, MONTH_SHORT_NP,
    NUMBER_NP, WEEK_EN, WEEK_SHORT_EN, WEEK_NP, WEEK_SHORT_NP
)

# -----------------------------------------------------------------------------------
# Type Aliases
# -----------------------------------------------------------------------------------
# DateFormatter represents a function that takes a NepaliDate object
# and returns its string representation according to a specific format.
DateFormatter = Callable[["NepaliDate"], str]


# -----------------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------------
def pad(n: int) -> str:
    """
    Pads a number with a leading zero if it is less than 10.
    For example: 5 -> "05", 12 -> "12".
    """
    return f"{n:02d}" if n < 10 else str(n)


def np_digit(s: str) -> str:
    """
    Converts a string of Arabic numerals to Nepali digits.
    For example: "123" -> "१२३".
    """
    return ''.join(NUMBER_NP[ord(c) - 48] for c in s)


# -----------------------------------------------------------------------------------
# Year Formatters
# -----------------------------------------------------------------------------------
def year_en(size: int) -> DateFormatter:
    """
    Returns a formatter for the year in English numerals.

    Parameters:
        size (int): Number of digits or variant.
            - 1 or 2: last 2 digits
            - 3: last 3 digits
            - >3: full year

    Returns:
        DateFormatter: Function to format NepaliDate.year
    """
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
    """
    Returns a formatter for the year in Nepali digits.

    Parameters:
        size (int): Number of digits or variant.

    Returns:
        DateFormatter: Function to format NepaliDate.year in Devanagari.
    """
    from NepaliDate import NepaliDate

    def f(date: "NepaliDate") -> str:
        y = str(date.year)
        if size <= 2:
            return np_digit(y[-2:])
        if size == 3:
            return np_digit(y[-3:])
        return np_digit(y)
    return f


# -----------------------------------------------------------------------------------
# Month Formatters
# -----------------------------------------------------------------------------------
def month_en(size: int) -> DateFormatter:
    """
    Returns a formatter for months in English transliteration.

    Parameters:
        size (int):
            - 1: numeric month without leading zero
            - 2: numeric month with leading zero
            - 3: short month name
            - >3: full month name
    """
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
    """
    Returns a formatter for months in Nepali (Devanagari) script.

    Parameters:
        size (int): same variants as month_en

    Returns:
        DateFormatter: Function to format NepaliDate.month
    """
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


# -----------------------------------------------------------------------------------
# Day/Week Formatters
# -----------------------------------------------------------------------------------
def date_en(size: int) -> DateFormatter:
    """
    Returns a formatter for the day or weekday in English.

    Parameters:
        size (int):
            - 1: numeric day without leading zero
            - 2: numeric day with leading zero
            - 3: short weekday name
            - >3: full weekday name
    """
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
    """
    Returns a formatter for the day or weekday in Nepali (Devanagari).

    Parameters:
        size (int): same variants as date_en

    Returns:
        DateFormatter: Function to format NepaliDate.day or weekday
    """
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


# -----------------------------------------------------------------------------------
# Fixed String Formatter
# -----------------------------------------------------------------------------------
def pass_str(seq: str) -> DateFormatter:
    """
    Returns a formatter that always outputs a fixed string.

    Parameters:
        seq (str): string to output

    Returns:
        DateFormatter: Function that ignores the date and returns seq
    """
    return lambda date: seq


# -----------------------------------------------------------------------------------
# Format Character Mapping
# -----------------------------------------------------------------------------------
# Maps format characters to their respective formatter functions.
fn = {
    'Y': year_en,
    'y': year_np,
    'M': month_en,
    'm': month_np,
    'D': date_en,
    'd': date_np,
}


# -----------------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------------
def is_special(ch: str) -> bool:
    """
    Checks if a character is a special format character.
    """
    return ch in fn


def tokenize(format_str: str) -> List[DateFormatter]:
    """
    Tokenizes a format string into a list of DateFormatter functions.

    Handles:
        - Repeated format characters for size (e.g., YYYY, yy)
        - Literal strings enclosed in double quotes
        - Sequential literal text outside quotes
    """
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


# -----------------------------------------------------------------------------------
# Main Formatting Function
# -----------------------------------------------------------------------------------
def format_date(nepali_date: "NepaliDate", format_str: str) -> str:
    """
    Formats a NepaliDate object according to a format string.

    Parameters:
        nepali_date (NepaliDate): date object to format
        format_str (str): format string containing special characters and literals

    Returns:
        str: formatted date string
    """
    return ''.join(f(nepali_date) for f in tokenize(format_str))
