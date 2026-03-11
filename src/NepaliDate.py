from datetime import datetime, timezone
from typing import Tuple, Union
from Helper import NEPALI_DATE_MAP, EPOCH, format_date

# -----------------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------------


def _parse(date_string: str) -> Tuple[int, int, int]:
    """
    Parses a Nepali date string into components (year, month, day).

    Supports separators: '-', '.', '/'
    If month or day is missing, defaults to 1.
    Month returned is 0-indexed internally.

    Raises:
        ValueError: If the date is invalid or out of supported Nepali date range.

    Returns:
        Tuple[int, int, int]: (year, month_indexed_from_0, day)
    """
    import re

    # Split the date string using allowed separators
    parts = re.split(r"[-./]", date_string, maxsplit=2)
    try:
        year = int(parts[0])
        month = int(parts[1]) if len(parts) > 1 else 1
        day = int(parts[2]) if len(parts) > 2 else 1
    except ValueError:
        raise ValueError("Invalid date")

    # Validate year
    if year < NEPALI_DATE_MAP[0]["year"] or year >= NEPALI_DATE_MAP[0]["year"] + len(NEPALI_DATE_MAP):
        raise ValueError("Nepal year out of range")

    # Validate month
    if month < 1 or month > 12:
        raise ValueError("Invalid Nepali month must be between 1 - 12")

    # Validate day
    days_in_month = NEPALI_DATE_MAP[year -
                                    NEPALI_DATE_MAP[0]["year"]]["days"][month - 1]
    if day < 1 or day > days_in_month:
        raise ValueError(
            f"Invalid Nepali date must be between 1 - {days_in_month} in {year}-{month}")

    return year, month - 1, day


# -----------------------------------------------------------------------------------
# NepaliDate Class
# -----------------------------------------------------------------------------------
class NepaliDate:
    """
    Represents a Nepali calendar date.

    Can be initialized using:
        - Gregorian datetime
        - Another NepaliDate object
        - Nepali year, month, day integers
        - Nepali date string (e.g., "2080-01-15")
        - Millisecond timestamp since epoch
    """

    def __init__(self, year_or_date: Union[datetime, 'NepaliDate', int, str] = None,
                 month: int = None, day: int = None):
        self.timestamp: datetime = None  # Corresponding Gregorian datetime
        self.year: int = None            # Nepali year
        self.month: int = None           # Nepali month (0-indexed internally)
        self.day: int = None             # Nepali day

        # Initialize based on type of input
        if year_or_date is None:
            self.set_english_date(datetime.now())
        elif isinstance(year_or_date, datetime):
            self.set_english_date(year_or_date)
        elif isinstance(year_or_date, NepaliDate):
            self.timestamp = year_or_date.timestamp
            self.year = year_or_date.year
            self.month = year_or_date.month
            self.day = year_or_date.day
        elif isinstance(year_or_date, str):
            self.set(*_parse(year_or_date))
        elif isinstance(year_or_date, int) and month is not None and day is not None:
            self.set(year_or_date, month, day)
        elif isinstance(year_or_date, int):
            # Treat as Unix timestamp in milliseconds
            self.set_english_date(datetime.fromtimestamp(year_or_date / 1000))
        else:
            raise ValueError("Invalid argument syntax")

    # -----------------------------------------------------------------------------------
    # Conversion from Gregorian date
    # -----------------------------------------------------------------------------------
    def set_english_date(self, date: datetime):
        """
        Converts a Gregorian datetime to Nepali date and updates instance attributes.

        Parameters:
            date (datetime): Gregorian date to convert.
        """
        self.timestamp = date

        # Convert to UTC timestamp in milliseconds
        utc_time = int(datetime(date.year, date.month, date.day,
                       tzinfo=timezone.utc).timestamp() * 1000)
        days_count = (utc_time - EPOCH) // 86400000  # total days since epoch
        idx = days_count // 366  # approximate index in NEPALI_DATE_MAP

        # Find correct year block
        while days_count >= NEPALI_DATE_MAP[idx]["daysTillNow"]:
            idx += 1

        prev_till_now = NEPALI_DATE_MAP[idx -
                                        1]["daysTillNow"] if idx - 1 >= 0 else 0
        days_count -= prev_till_now

        tmp = NEPALI_DATE_MAP[idx]
        self.year = tmp["year"]
        self.month = 0

        # Find the correct month
        while days_count >= tmp["days"][self.month]:
            days_count -= tmp["days"][self.month]
            self.month += 1

        self.day = days_count + 1

    # -----------------------------------------------------------------------------------
    # Set Nepali date manually
    # -----------------------------------------------------------------------------------
    def set(self, year: int, month: int, date: int):
        """
        Sets Nepali date and calculates the equivalent Gregorian date.

        Parameters:
            year (int): Nepali year
            month (int): Nepali month (0-indexed internally)
            date (int): Nepali day
        """
        idx = year + (month // 12) - NEPALI_DATE_MAP[0]["year"]
        if idx < 0 or idx >= len(NEPALI_DATE_MAP):
            raise ValueError("Nepal year out of range!")

        tmp = NEPALI_DATE_MAP[idx]
        d = tmp["daysTillNow"] - sum(tmp["days"])

        # Handle month rollover
        m = month % 12
        mm = m if m >= 0 else 12 + m

        for i in range(mm):
            d += tmp["days"][i]

        d += date - 1

        # Compute UTC timestamp
        utc_timestamp = EPOCH + d * 86400000
        utc_date = datetime.fromtimestamp(
            utc_timestamp / 1000, tz=timezone.utc)

        # Set the Gregorian and Nepali date
        self.set_english_date(utc_date)

    # -----------------------------------------------------------------------------------
    # Date Formatting
    # -----------------------------------------------------------------------------------
    def format(self, format_str: str) -> str:
        """
        Formats the Nepali date according to a format string.

        Parameters:
            format_str (str): e.g., 'YYYY/MM/DD' or custom string with JS-style formatters

        Returns:
            str: Formatted Nepali date string
        """
        return format_date(self, format_str)

    # -----------------------------------------------------------------------------------
    # String Representation
    # -----------------------------------------------------------------------------------
    def __str__(self) -> str:
        """
        Returns Nepali date as a string 'YYYY/MM/DD'.
        Month is converted to 1-indexed for display.
        """
        return f"{self.year}/{self.month + 1}/{self.day}"
