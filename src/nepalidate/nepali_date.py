from datetime import datetime, timezone
from typing import Tuple, Union
from .helper.constants import nepali_date_map, EPOCH
from .helper.date_formatter import format_date


# -----------------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------------
def _parse(date_string: str) -> Tuple[int, int, int]:
    """
    Parse a Nepali date string into year, month, and day components.

    The function supports multiple separators (`-`, `/`, `.`).
    If month or day is missing, they default to `1`.

    Internally, the month is returned as **0-indexed** for easier
    processing with the Nepali date map.

    Args:
        date_string (str):
            Nepali date string (e.g. `"2080-01-15"`, `"2080/1/15"`).

    Raises:
        ValueError:
            - If the string cannot be parsed into numbers.
            - If the year is outside the supported Nepali calendar range.
            - If the month is not between 1–12.
            - If the day exceeds the number of days in that Nepali month.

    Returns:
        Tuple[int, int, int]:
            A tuple `(year, month_index, day)` where month is 0-indexed.

    Example:
        >>> _parse("2080-05-10")
        (2080, 4, 10)
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
    if year < nepali_date_map[0]["year"] or year >= nepali_date_map[0]["year"] + len(nepali_date_map):
        raise ValueError("Nepal year out of range")

    # Validate month
    if month < 1 or month > 12:
        raise ValueError("Invalid Nepali month must be between 1 - 12")

    # Validate day
    days_in_month = nepali_date_map[year -
                                    nepali_date_map[0]["year"]]["days"][month - 1]
    if day < 1 or day > days_in_month:
        raise ValueError(
            f"Invalid Nepali date must be between 1 - {days_in_month} in {year}-{month}")

    return year, month - 1, day


# -----------------------------------------------------------------------------------
# NepaliDate Class
# -----------------------------------------------------------------------------------
class NepaliDate:
    """
    Represents a date in the Nepali (Bikram Sambat) calendar.

    This class provides functionality to:
        - Convert between Nepali and Gregorian dates
        - Parse Nepali date strings
        - Format Nepali dates using custom format strings
        - Retrieve the equivalent Gregorian date

    Internally, Nepali months are **stored as 0-indexed** for calculations
    but displayed as **1-indexed** when converted to strings.

    Attributes:
        timestamp (datetime):
            Equivalent Gregorian datetime.
        year (int):
            Nepali year (Bikram Sambat).
        month (int):
            Nepali month (0-indexed internally).
        day (int):
            Nepali day of the month.
    """

    def __init__(self, year_or_date: Union[datetime, 'NepaliDate', int, str] = None,
                 month: int = None, day: int = None):
        """
        Initialize a NepaliDate instance.

        The constructor supports multiple input types:

        - No arguments → current date
        - Gregorian datetime
        - Another NepaliDate instance
        - Nepali date string
        - Nepali year, month, day integers
        - Unix timestamp in milliseconds

        Args:
            year_or_date:
                Can be:
                - datetime → Gregorian date
                - NepaliDate → copy constructor
                - str → Nepali date string
                - int → timestamp or Nepali year
            month (int, optional):
                Nepali month (1–12 when provided externally).
            day (int, optional):
                Nepali day of month.

        Raises:
            ValueError:
                If the argument combination is invalid.
        """
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
        Convert a Gregorian datetime to a Nepali date.

        Updates the object's internal Nepali date fields
        (`year`, `month`, `day`) as well as the stored timestamp.

        Args:
            date (datetime):
                Gregorian date to convert.

        Example:
            >>> nd = NepaliDate()
            >>> nd.set_english_date(datetime(2023, 4, 14))
        """
        self.timestamp = date

        # Convert to UTC timestamp in milliseconds
        utc_time = int(datetime(date.year, date.month, date.day,
                       tzinfo=timezone.utc).timestamp() * 1000)
        days_count = (utc_time - EPOCH) // 86400000  # total days since epoch
        idx = days_count // 366  # approximate index in nepali_date_map

        # Find correct year block
        while days_count >= nepali_date_map[idx]["daysTillNow"]:
            idx += 1

        prev_till_now = nepali_date_map[idx -
                                        1]["daysTillNow"] if idx - 1 >= 0 else 0
        days_count -= prev_till_now

        tmp = nepali_date_map[idx]
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
        Set the Nepali date manually and compute the equivalent
        Gregorian timestamp.

        Args:
            year (int):
                Nepali year.
            month (int):
                Nepali month (0-indexed internally).
            date (int):
                Nepali day.

        Raises:
            ValueError:
                If the year is outside the supported Nepali calendar range.
        """
        idx = year + (month // 12) - nepali_date_map[0]["year"]
        if idx < 0 or idx >= len(nepali_date_map):
            raise ValueError("Nepal year out of range!")

        tmp = nepali_date_map[idx]
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
        Format the Nepali date using a custom format string.

        Formatting tokens are interpreted by the `format_date` helper.

        Args:
            format_str (str):
                Format pattern such as `"YYYY/MM/DD"`.

        Returns:
            str:
                Formatted Nepali date string.

        Example:
            >>> nd = NepaliDate("2080-01-01")
            >>> nd.format("YYYY/MM/DD")
            '2080/01/01'
        """
        return format_date(self, format_str)

    # -----------------------------------------------------------------------------------
    # String Representation
    # -----------------------------------------------------------------------------------
    def __str__(self) -> str:
        """
        Return the Nepali date in `YYYY/MM/DD` format.

        Returns:
            str: Nepali date string.

        Example:
            >>> str(NepaliDate("2080-01-01"))
            '2080/1/1'
        """
        return f"{self.year}/{self.month + 1}/{self.day}"

    # -------------------------------------------------------------------------
    # Get Gregorian Date
    # -------------------------------------------------------------------------
    def get_english_date(self) -> datetime:
        """
        Return the Gregorian (English) datetime equivalent of the Nepali date.

        This is the internally stored timestamp generated during
        initialization or when the date was last updated.

        Returns:
            datetime:
                Gregorian datetime corresponding to the Nepali date.

        Example:
            >>> nd = NepaliDate("2080-01-01")
            >>> nd.get_english_date()
            datetime.datetime(2023, 4, 14, tzinfo=datetime.timezone.utc)
        """
        return self.timestamp
