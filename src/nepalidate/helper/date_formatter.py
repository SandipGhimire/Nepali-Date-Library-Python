from typing import Callable, List
from .constants import (
    month_en, month_short_en, month_short_np, month_np,
    number_np, week_short_np, week_short_en, week_np, week_en
)

# -----------------------------------------------------------------------------
# Type Aliases
# -----------------------------------------------------------------------------
DateFormatter = Callable[["NepaliDate"], str]
"""
Represents a formatter function that converts a NepaliDate object
into a formatted string.

The function receives a `NepaliDate` instance and returns a string
representation of a specific component (year, month, day, etc.)
according to a formatting rule.
"""


# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------
def pad(n: int) -> str:
    """
    Pad a number with a leading zero if it is less than 10.

    Args:
        n (int): Number to pad.

    Returns:
        str: Zero-padded string.

    Example:
        >>> pad(5)
        '05'
        >>> pad(12)
        '12'
    """
    return f"{n:02d}" if n < 10 else str(n)


def np_digit(s: str) -> str:
    """
    Convert Arabic numerals in a string to Nepali (Devanagari) digits.

    Args:
        s (str): String containing numeric characters.

    Returns:
        str: String with digits converted to Nepali numerals.

    Example:
        >>> np_digit("123")
        '१२३'
    """
    return ''.join(number_np[ord(c) - 48] for c in s)


# -----------------------------------------------------------------------------
# Year Formatters
# -----------------------------------------------------------------------------
def year_en(size: int) -> DateFormatter:
    """
    Create a formatter for the Nepali year using English digits.

    Args:
        size (int):
            Determines the formatting style:
            - 1 or 2 → last 2 digits of the year
            - 3 → last 3 digits
            - ≥4 → full year

    Returns:
        DateFormatter: Formatter function.
    """
    from nepali_date import NepaliDate

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
    Create a formatter for the Nepali year using Nepali digits.

    Args:
        size (int):
            Determines the formatting style.

    Returns:
        DateFormatter: Formatter function producing Devanagari digits.
    """
    from nepali_date import NepaliDate

    def f(date: "NepaliDate") -> str:
        y = str(date.year)

        if size <= 2:
            return np_digit(y[-2:])

        if size == 3:
            return np_digit(y[-3:])

        return np_digit(y)

    return f


# -----------------------------------------------------------------------------
# Month Formatters
# -----------------------------------------------------------------------------
def month_en(size: int) -> DateFormatter:
    """
    Create a formatter for Nepali months using English names or digits.

    Args:
        size (int):
            - 1 → month number without leading zero
            - 2 → month number with leading zero
            - 3 → abbreviated English month name
            - ≥4 → full English month name

    Returns:
        DateFormatter: Formatter function.
    """
    from nepali_date import NepaliDate

    def f(date: "NepaliDate") -> str:
        m = date.month

        if size == 1:
            return str(m + 1)

        if size == 2:
            return pad(m + 1)

        if size == 3:
            return month_short_en[m]

        return month_en[m]

    return f


def month_np(size: int) -> DateFormatter:
    """
    Create a formatter for Nepali months using Nepali script.

    Args:
        size (int):
            Same format behavior as `month_en`.

    Returns:
        DateFormatter: Formatter function using Nepali digits or names.
    """
    from nepali_date import NepaliDate

    def f(date: "NepaliDate") -> str:
        m = date.month

        if size == 1:
            return np_digit(str(m + 1))

        if size == 2:
            return np_digit(pad(m + 1))

        if size == 3:
            return month_short_np[m]

        return month_np[m]

    return f


# -----------------------------------------------------------------------------
# Day / Weekday Formatters
# -----------------------------------------------------------------------------
def date_en(size: int) -> DateFormatter:
    """
    Create a formatter for the day or weekday in English.

    Args:
        size (int):
            - 1 → numeric day
            - 2 → numeric day with leading zero
            - 3 → abbreviated weekday
            - ≥4 → full weekday name

    Returns:
        DateFormatter: Formatter function.
    """
    from nepali_date import NepaliDate

    def f(date: "NepaliDate") -> str:
        d = date.day

        if size == 1:
            return str(d)

        if size == 2:
            return pad(d)

        if size == 3:
            return week_short_en[date.weekday()]

        return week_en[date.weekday()]

    return f


def date_np(size: int) -> DateFormatter:
    """
    Create a formatter for the day or weekday in Nepali script.

    Args:
        size (int):
            Same format behavior as `date_en`.

    Returns:
        DateFormatter: Formatter function using Nepali digits or weekday names.
    """
    from nepali_date import NepaliDate

    def f(date: "NepaliDate") -> str:
        d = date.day

        if size == 1:
            return np_digit(str(d))

        if size == 2:
            return np_digit(pad(d))

        if size == 3:
            return week_short_np[date.weekday()]

        return week_np[date.weekday()]

    return f


# -----------------------------------------------------------------------------
# Fixed String Formatter
# -----------------------------------------------------------------------------
def pass_str(seq: str) -> DateFormatter:
    """
    Create a formatter that always returns a fixed string.

    Useful for literal text inside format strings.

    Args:
        seq (str): Literal text.

    Returns:
        DateFormatter: Formatter function.
    """
    return lambda date: seq


# -----------------------------------------------------------------------------
# Format Character Mapping
# -----------------------------------------------------------------------------
fn = {
    'Y': year_en,
    'y': year_np,
    'M': month_en,
    'm': month_np,
    'D': date_en,
    'd': date_np,
}
"""
Mapping between format characters and their corresponding formatter
factory functions.

Examples:
    Y → English year formatter
    y → Nepali year formatter
    M → English month formatter
    m → Nepali month formatter
    D → English day formatter
    d → Nepali day formatter
"""


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def is_special(ch: str) -> bool:
    """
    Determine whether a character is a special formatting token.

    Args:
        ch (str): Character to test.

    Returns:
        bool: True if the character represents a formatter token.
    """
    return ch in fn


def tokenize(format_str: str) -> List[DateFormatter]:
    """
    Convert a format string into a list of formatter functions.

    The tokenizer processes:

    • Repeated format characters (e.g., YYYY, MM, DD)  
    • Literal strings enclosed in double quotes  
    • Plain text outside quotes  

    Args:
        format_str (str): Formatting pattern.

    Returns:
        List[DateFormatter]: List of formatter functions.
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


# -----------------------------------------------------------------------------
# Main Formatting Function
# -----------------------------------------------------------------------------
def format_date(nepali_date: "NepaliDate", format_str: str) -> str:
    """
    Format a NepaliDate object according to a custom format string.

    Args:
        nepali_date (NepaliDate):
            Nepali date instance to format.

        format_str (str):
            Format pattern using special characters.

            Examples:
                YYYY → full year  
                MM → month number  
                DD → day number  

    Returns:
        str: Formatted date string.

    Example:
        >>> format_date(nd, "YYYY-MM-DD")
        '2080-01-01'

        >>> format_date(nd, "DD MMMM YYYY")
        '01 Baisakh 2080'
    """
    return ''.join(f(nepali_date) for f in tokenize(format_str))
