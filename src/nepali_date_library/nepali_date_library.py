from datetime import datetime, timezone, timedelta
from typing import Tuple, Union, Dict, List
from .helper.constants import (
    nepali_date_map,
    EPOCH,
    month_short_np, month_np, month_short_en, month_en,
    week_en, week_np, week_short_en, week_short_np
)
from .helper.date_formatter import format_date
import math


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
        raise ValueError(f"Nepal year out of range, Year: {year}")

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

    def clone(self) -> "NepaliDate":
        """
        Create a copy of the current NepaliDate instance.

        Returns:
            NepaliDate: A new instance with the same date and time.
        """
        return NepaliDate(self)

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

    # -------------------------------------------------------------------------
    # Parse Nepali Date String
    # -------------------------------------------------------------------------
    def parse(self, date_string: str) -> None:
        """
        Parse a Nepali date string and update the current instance.

        Args:
            date_string (str): Nepali date string (e.g., "2080-01-15").

        Raises:
            ValueError: If the date string format is invalid or out of range.
        """
        self.set(*_parse(date_string))

    # -------------------------------------------------------------------------
    # Get Year
    # -------------------------------------------------------------------------
    def get_year(self) -> int:
        """
        Return the Nepali year (Bikram Sambat).

        Returns:
            int: Nepali year.
        """
        return self.year

    # -------------------------------------------------------------------------
    # Get Month
    # -------------------------------------------------------------------------
    def get_month(self) -> int:
        """
        Return the Nepali month (0-indexed internally).

        Returns:
            int: Nepali month index (0-11).
        """
        return self.month

    # -------------------------------------------------------------------------
    # Get Day of Week
    # -------------------------------------------------------------------------
    def get_day(self) -> int:
        """
        Return the day of the week (0-6, where 0 is Monday).

        Returns:
            int: Day of the week index.
        """
        return self.timestamp.weekday()

    # -------------------------------------------------------------------------
    # Get Day of Month
    # -------------------------------------------------------------------------
    def get_date(self) -> int:
        """
        Return the Nepali day of the month.

        Returns:
            int: Day of the month (1-32).
        """
        return self.day

    # -------------------------------------------------------------------------
    # Set Year
    # -------------------------------------------------------------------------
    def set_year(self, year: int) -> None:
        """
        Set the Nepali year.

        Args:
            year (int): New Nepali year.
        """
        self.set(year, self.month, self.day)

    # -------------------------------------------------------------------------
    # Set Month
    # -------------------------------------------------------------------------
    def set_month(self, month: int) -> None:
        """
        Set the Nepali month.

        Args:
            month (int): New Nepali month (0-11).
        """
        self.set(self.year, month, self.day)

    # -------------------------------------------------------------------------
    # Set Day of Month
    # -------------------------------------------------------------------------
    def set_date(self, day: int) -> None:
        """
        Set the Nepali day of the month.

        Args:
            day (int): New Nepali day of the month (1-32).
        """
        self.set(self.year, self.month, day)

    # -------------------------------------------------------------------------
    # Add Days
    # -------------------------------------------------------------------------
    def add_days(self, days: int) -> 'NepaliDate':
        """
        Add the specified number of days to the current Nepali date.

        Args:
            days (int): Number of days to add (can be negative).

        Returns:
            NepaliDate: A new NepaliDate instance with the added days.
        """
        new_timestamp = self.timestamp + timedelta(days=days)
        return NepaliDate(new_timestamp)

    # -------------------------------------------------------------------------
    # Add Months
    # -------------------------------------------------------------------------
    def add_months(self, months: int) -> 'NepaliDate':
        """
        Add the specified number of months to the current Nepali date.

        If the target month has fewer days than the current day,
        the day is capped at the last day of the target month.

        Args:
            months (int): Number of months to add (can be negative).

        Returns:
            NepaliDate: A new NepaliDate instance with the added months.

        Raises:
            ValueError: If the resulting date is outside the supported range.
        """
        new_year = self.year
        new_month = self.month + months

        new_year += new_month // 12
        new_month = new_month % 12

        if new_month < 0:
            new_month += 12
            new_year -= 1

        year_index = new_year - nepali_date_map[0]["year"]

        if year_index < 0 or year_index >= len(nepali_date_map):
            raise ValueError("Resulting date is out of supported range")

        days_in_new_month = nepali_date_map[year_index]["days"][new_month]

        new_day = min(self.day, days_in_new_month)

        return NepaliDate(new_year, new_month, new_day)

    # -------------------------------------------------------------------------
    # Add Years
    # -------------------------------------------------------------------------
    def add_years(self, years: int) -> 'NepaliDate':
        """
        Add the specified number of years to the current Nepali date.

        If the current day/month does not exist in the target year
        (e.g., leap day), the day is capped.

        Args:
            years (int): Number of years to add (can be negative).

        Returns:
            NepaliDate: A new NepaliDate instance with the added years.

        Raises:
            ValueError: If the resulting date is outside the supported range.
        """
        new_year = self.year + years

        if new_year < nepali_date_map[0]["year"] or new_year >= nepali_date_map[0]["year"] + len(nepali_date_map):
            raise ValueError("Resulting date is out of supported range")

        year_index = new_year - nepali_date_map[0]["year"]

        days_in_new_year_month = nepali_date_map[year_index]["days"][self.month]
        new_day = min(self.day, days_in_new_year_month)

        return NepaliDate(new_year, self.month, new_day)

    # -------------------------------------------------------------------------
    # Minimum Date
    # -------------------------------------------------------------------------
    @staticmethod
    def minimum() -> datetime:
        """
        Return the earliest Gregorian date supported by the Nepali calendar.

        Returns:
            datetime: Minimum supported Gregorian date.
        """
        return datetime.fromtimestamp(EPOCH / 1000, tz=timezone.utc)

    # -------------------------------------------------------------------------
    # Maximum Date
    # -------------------------------------------------------------------------
    @staticmethod
    def maximum() -> datetime:
        """
        Return the latest Gregorian date supported by the Nepali calendar.

        Returns:
            datetime: Maximum supported Gregorian date.
        """
        return datetime.fromtimestamp((EPOCH + (nepali_date_map[-1]["daysTillNow"] * 86400000)) / 1000, tz=timezone.utc)

    # -------------------------------------------------------------------------
    # Days in Month
    # -------------------------------------------------------------------------
    def days_in_month(self) -> int:
        """
        Return the number of days in the current Nepali month.

        Returns:
            int: Number of days in the month.
        """
        year_index = self.year - nepali_date_map[0]["year"]
        return nepali_date_map[year_index]["days"][self.month]

    # -------------------------------------------------------------------------
    # Is Leap Year
    # -------------------------------------------------------------------------
    def is_leap_year(self) -> bool:
        """
        Check if the current Nepali year is a leap year (366 days or more).

        Returns:
            bool: True if it is a leap year, False otherwise.
        """
        year_index = self.year - nepali_date_map[0]["year"]
        return nepali_date_map[year_index]["totalDays"] >= 366

    # -------------------------------------------------------------------------
    # Get Weeks in Month
    # -------------------------------------------------------------------------
    def get_weeks_in_month(self) -> int:
        """
        Calculate the number of weeks in the current Nepali month.

        Returns:
            int: Number of weeks.
        """
        first_day = NepaliDate(self.year, self.month, 1)
        first_day_of_week = first_day.get_day()
        total_days = self.days_in_month()
        return math.ceil((total_days + first_day_of_week) / 7)

    # -------------------------------------------------------------------------
    # Difference between two dates
    # -------------------------------------------------------------------------
    def diff(self, date: "NepaliDate", unit: str) -> int:
        """
        Calculate the difference between two dates in the specified unit.

        Args:
            date (NepaliDate): Date to compare with.
            unit (str): Unit for the difference ('day', 'month', or 'year').

        Returns:
            int: Difference value in the specified unit.

        Raises:
            ValueError: If an invalid unit is provided.
        """
        if unit == "day":
            ts1 = self.timestamp.replace(tzinfo=None)
            ts2 = date.timestamp.replace(tzinfo=None)
            delta = ts1 - ts2
            return delta.days

        elif unit == "month":
            year_diff = self.year - date.year
            month_diff = self.month - date.month
            return year_diff * 12 + month_diff

        elif unit == "year":
            return self.year - date.year

        else:
            raise ValueError("Invalid unit for diff calculation")

    # -------------------------------------------------------------------------
    # Start of Day
    # -------------------------------------------------------------------------
    def start_of_day(self) -> "NepaliDate":
        """
        Return a new NepaliDate instance representing the start of the current day.

        Returns:
            NepaliDate: New instance set to 00:00:00.
        """
        start = self.timestamp.replace(
            hour=0, minute=0, second=0, microsecond=0)
        return NepaliDate(start)

    # -------------------------------------------------------------------------
    # End of Day
    # -------------------------------------------------------------------------
    def end_of_day(self) -> "NepaliDate":
        """
        Return a new NepaliDate instance representing the end of the current day.

        Returns:
            NepaliDate: New instance set to 23:59:59.999.
        """
        end = self.timestamp.replace(
            hour=23, minute=59, second=59, microsecond=999000)
        return NepaliDate(end)

    # -------------------------------------------------------------------------
    # Start of Week
    # -------------------------------------------------------------------------
    def start_of_week(self, start_of_week: int = 0) -> "NepaliDate":
        """
        Return a new NepaliDate instance representing the start of the week.

        Args:
            start_of_week (int): Day to consider as start of week (0-6, default 0 for Monday).

        Returns:
            NepaliDate: New instance set to the first day of the week.

        Raises:
            ValueError: If start_of_week is not between 0 and 6.
        """
        if start_of_week < 0 or start_of_week > 6:
            raise ValueError(
                "start_of_week mush be an integer between 0 and 6")

        current_day = self.get_day()
        day_to_subtract = (current_day - start_of_week + 7) % 7
        result = self.clone().start_of_day()
        result = result.add_days(-day_to_subtract)
        return result

    # -------------------------------------------------------------------------
    # End of Week
    # -------------------------------------------------------------------------
    def end_of_week(self, start_of_week: int = 0) -> "NepaliDate":
        """
        Return a new NepaliDate instance representing the end of the week.

        Args:
            start_of_week (int): Day to consider as start of week (0-6).

        Returns:
            NepaliDate: New instance set to the last day of the week.
        """
        if start_of_week < 0 or start_of_week > 6:
            raise ValueError(
                "start_of_week mush be an integer between 0 and 6")

        start_of_week = self.start_of_week(start_of_week)
        return start_of_week.add_days(6).end_of_day()

    # -------------------------------------------------------------------------
    # Start of Month
    # -------------------------------------------------------------------------
    def start_of_month(self) -> "NepaliDate":
        """
        Return a new NepaliDate instance representing the start of the current month.

        Returns:
            NepaliDate: New instance set to the 1st day of the month.
        """
        return NepaliDate(self.year, self.month, 1).start_of_day()

    # -------------------------------------------------------------------------
    # End of Month
    # -------------------------------------------------------------------------
    def end_of_month(self) -> "NepaliDate":
        """
        Return a new NepaliDate instance representing the end of the current month.

        Returns:
            NepaliDate: New instance set to the last day of the month.
        """
        return NepaliDate(self.year, self.month, self.days_in_month()).end_of_day()

    # -------------------------------------------------------------------------
    # Start of Year
    # -------------------------------------------------------------------------
    def start_of_year(self) -> "NepaliDate":
        """
        Return a new NepaliDate instance representing the start of the current year.

        Returns:
            NepaliDate: New instance set to the 1st day of the first month (Baisakh).
        """
        return NepaliDate(self.year, 0, 1).start_of_day()

    # -------------------------------------------------------------------------
    # End of Year
    # -------------------------------------------------------------------------
    def end_of_year(self) -> "NepaliDate":
        """
        Return a new NepaliDate instance representing the end of the current year.

        Returns:
            NepaliDate: New instance set to the last day of the last month (Chaitra).
        """
        year_index = self.year - nepali_date_map[0]["year"]
        days_in_chaitra = nepali_date_map[year_index]["days"][11]
        return NepaliDate(self.year, 11, days_in_chaitra).end_of_day()

    # -------------------------------------------------------------------------
    # Get Month Name
    # -------------------------------------------------------------------------
    @staticmethod
    def get_month_name(month: int, short: bool = False, nepali: bool = False) -> str:
        """
        Return the name of the specified Nepali month.

        Args:
            month (int): Month index (0-11).
            short (bool): If True, return the short form of the month name.
            nepali (bool): If True, return the name in Nepali script.

        Returns:
            str: Month name.

        Raises:
            ValueError: If the month index is invalid.
        """
        if month < 0 or month > 11:
            raise ValueError("Invalid month index, must be between 0-11")

        result = ""
        if nepali:
            result = month_short_np[month] if short else month_np[month]
        else:
            result = month_short_en[month] if short else month_en[month]

        return result

    # -------------------------------------------------------------------------
    # Get Day Name
    # -------------------------------------------------------------------------
    @staticmethod
    def get_day_name(day: int, short: bool = False, nepali: bool = False) -> str:
        """
        Return the name of the specified day of the week.

        Args:
            day (int): Day index (0-6, where 0 is Monday).
            short (bool): If True, return the short form of the day name.
            nepali (bool): If True, return the name in Nepali script.

        Returns:
            str: Day name.

        Raises:
            ValueError: If the day index is invalid.
        """
        if day < 0 or day > 6:
            raise ValueError("Invalid day index, must be between 0-6")

        if nepali:
            result = week_short_np[day] if short else week_np[day]
        else:
            result = week_short_en[day] if short else week_en[day]

        return result

    # -------------------------------------------------------------------------
    # Is Valid
    # -------------------------------------------------------------------------
    @staticmethod
    def is_valid(year: int, month: int, date: int) -> bool:
        """
        Check if the specified Nepali date is valid.

        Args:
            year (int): Nepali year.
            month (int): Nepali month index (0-11).
            date (int): Nepali day of the month.

        Returns:
            bool: True if the date is valid within the supported range.
        """
        if year < nepali_date_map[0]["year"] or year >= nepali_date_map[0]["year"] + len(nepali_date_map):
            return False

        if month < 0 or month > 11:
            return False

        year_index = year - nepali_date_map[0]["year"]
        days_in_month = nepali_date_map[year_index]["days"][month]

        if date < 1 or date > days_in_month:
            return False

        return True

    # -------------------------------------------------------------------------
    # Is Current Valid
    # -------------------------------------------------------------------------
    def is_valid_instance(self) -> bool:
        """
        Check if the current NepaliDate instance contains a valid date.

        Returns:
            bool: True if valid, False otherwise.
        """
        return NepaliDate.is_valid(self.year, self.month, self.day)

    # -------------------------------------------------------------------------
    # Get Calendar Days
    # -------------------------------------------------------------------------
    @staticmethod
    def get_calendar_days(year: int, month: int) -> Dict:
        """
        Generate calendar grid days including leading/trailing days
        from adjacent months to fill a 6-week (42-cell) grid.
        """
        if not NepaliDate.is_valid(year, month, 1):
            raise ValueError("Invalid year or month")

        year_index = year - nepali_date_map[0]["year"]
        first_day = NepaliDate(year, month, 1)
        first_day_of_week = first_day.get_day()
        days_in_month = nepali_date_map[year_index]["days"][month]

        prev_month = month - 1
        prev_year = year
        if prev_month < 0:
            prev_month = 11
            prev_year -= 1

        next_month = month + 1
        next_year = year
        if next_month > 11:
            next_month = 0
            next_year += 1

        prev_days = []
        if prev_year >= nepali_date_map[0]["year"] and first_day_of_week > 0:
            prev_idx = prev_year - nepali_date_map[0]["year"]
            days_in_prev = nepali_date_map[prev_idx]["days"][prev_month]
            prev_days = list(
                range(days_in_prev - first_day_of_week + 1, days_in_prev + 1))

        current_days = list(range(1, days_in_month + 1))

        remaining = 42 - first_day_of_week - days_in_month
        next_days = list(range(1, remaining + 1)) if remaining > 0 else []

        return {
            "prev_remaining_days": first_day_of_week,
            "prev_month": {"year": prev_year, "month": prev_month, "days": prev_days},
            "current_month": {"year": year, "month": month, "days": current_days},
            "next_month": {"year": next_year, "month": next_month, "days": next_days},
            "remaining_days": remaining,
        }

    # -------------------------------------------------------------------------
    # Is After the Date
    # -------------------------------------------------------------------------
    def is_after(self, date: "NepaliDate") -> bool:
        """
        Check if this date comes after the specified date.

        Args:
            date (NepaliDate): Date to compare with.

        Returns:
            bool: True if this date is strictly after the specified date.
        """
        return self.timestamp > date.timestamp

    # -------------------------------------------------------------------------
    # Is Before the Date
    # -------------------------------------------------------------------------
    def is_before(self, date: "NepaliDate") -> bool:
        """
        Check if this date comes before the specified date.

        Args:
            date (NepaliDate): Date to compare with.

        Returns:
            bool: True if this date is strictly before the specified date.
        """
        return self.timestamp < date.timestamp

    # -------------------------------------------------------------------------
    # Is Equal to the Date
    # -------------------------------------------------------------------------
    def is_equal(self, date: "NepaliDate") -> bool:
        """
        Check if this date is equal to the specified date.

        Args:
            date (NepaliDate): Date to compare with.

        Returns:
            bool: True if both instances represent the same year, month, and day.
        """
        return self == date

    # -------------------------------------------------------------------------
    # Is Same as the Date
    # -------------------------------------------------------------------------
    def is_same(self, date: "NepaliDate", unit: str) -> bool:
        """
        Check if this date is the same as another date within a specified unit.

        Args:
            date (NepaliDate): Date to compare with.
            unit (str): Unit for comparison ('year', 'month', or 'day').

        Returns:
            bool: True if they are the same within the specified unit.

        Raises:
            ValueError: If an invalid unit is provided.
        """
        if unit == "year":
            return self.year == date.year
        elif unit == "month":
            return self.year == date.year and self.month == date.month
        elif unit == "day":
            return self.is_equal(date)
        else:
            raise ValueError("Invalid unit for same check")

    # -------------------------------------------------------------------------
    # Get Quarter
    # -------------------------------------------------------------------------
    def current_quarter_dates(self) -> Dict[str, "NepaliDate"]:
        """
        Return the start and end dates for a specific quarter of the current year.

        Returns:
            Dict[str, NepaliDate]: Dictionary with 'start' and 'end' keys.

        Raises:
            ValueError: If the quarter is invalid.
        """
        return NepaliDate.get_quarter(self.current_quarter(), self.year)

    # -------------------------------------------------------------------------
    # Get Quarter by Year
    # -------------------------------------------------------------------------
    @staticmethod
    def get_quarter(quarter: int, year: int) -> Dict[str, "NepaliDate"]:
        """
        Return the start and end dates for a specific quarter and year.

        Args:
            quarter (int): Quarter number (1-4).
            year (int): Nepali year.

        Returns:
            Dict[str, NepaliDate]: Dictionary with 'start' and 'end' keys.

        Raises:
            ValueError: If quarter or year is invalid.
        """
        if quarter < 1 or quarter > 4:
            raise ValueError("Invalid quarter, must be between 1-4")
        if nepali_date_map[year - nepali_date_map[0]["year"]] is None:
            raise ValueError("Invalid year")

        nepali_year = year
        start_month = (quarter - 1) * 3

        start = NepaliDate(nepali_year, start_month, 1)
        end = start.add_months(2).end_of_month()

        return {"start": start, "end": end}

    # -------------------------------------------------------------------------
    # Get Current Quarter
    # -------------------------------------------------------------------------
    def current_quarter(self) -> int:
        """
        Return the quarter number (1-4) for the current date.

        Returns:
            int: Current quarter number.
        """
        return self.month // 3 + 1

    # -------------------------------------------------------------------------
    # Get Quarters
    # -------------------------------------------------------------------------
    def current_year_quarters(self) -> List[Dict[str, "NepaliDate"]]:
        """
        Return the dates for all four quarters of the current year.

        Returns:
            List[Dict[str, NepaliDate]]: A list containing start/end for each quarter.
        """
        return NepaliDate.get_quarters(self.year)

    # -------------------------------------------------------------------------
    # Get Quarters by Year
    # -------------------------------------------------------------------------
    @staticmethod
    def get_quarters(year) -> List[Dict[str, "NepaliDate"]]:
        """
        Return the dates for all four quarters of a specified year.

        Args:
            year (int): Nepali year.

        Returns:
            List[Dict[str, NepaliDate]]: Dictionary mapping Q1-Q4 to their dates.

        Raises:
            ValueError: If the year is invalid.
        """
        if nepali_date_map[year - nepali_date_map[0]["year"]] is None:
            raise ValueError("Invalid year")

        nepali_year = year

        return {
            "Q1": NepaliDate.get_quarter(1, year),
            "Q2": NepaliDate.get_quarter(2, year),
            "Q3": NepaliDate.get_quarter(3, year),
            "Q4": NepaliDate.get_quarter(4, year)
        }

    # -------------------------------------------------------------------------
    # Get Current Fiscal Year
    # -------------------------------------------------------------------------
    @staticmethod
    def current_fiscal_year() -> int:
        """
        Return the current Nepali fiscal year.

        The fiscal year typically starts in Shrawan (Month 4, but here indexed).

        Returns:
            int: The starting year of the current fiscal year.
        """
        today = NepaliDate()
        year = today.get_year()
        month = today.get_month()
        return year - 1 if month < 3 else year

    # -------------------------------------------------------------------------
    # Get Fiscal Year Quarter
    # -------------------------------------------------------------------------
    @staticmethod
    def get_fiscal_quarter(quarter: int, fiscal_year: int = None) -> Dict[str, "NepaliDate"]:
        """
        Return the start and end dates for a specific fiscal year quarter.

        Args:
            quarter (int): Quarter number (1-4).
            fiscal_year (int, optional): The fiscal year. Defaults to current.

        Returns:
            Dict[str, NepaliDate]: Dictionary with 'start' and 'end' keys.

        Raises:
            ValueError: If the quarter is invalid.
        """
        if quarter < 1 or quarter > 4 or not isinstance(quarter, int):
            raise ValueError("Quarter must be an integer between 1 and 4")

        current_fiscal_year = fiscal_year or NepaliDate.current_fiscal_year()

        start_year = current_fiscal_year
        start_month = (quarter - 1) * 3 + 3

        if quarter == 4:
            start_year = current_fiscal_year + 1
            start_month = 0

        if start_month > 11:
            start_year += 1
            start_month -= 12

        end_month = start_month + 2
        end_year = start_year

        if end_month > 11:
            end_year += 1
            end_month -= 12

        start = NepaliDate(start_year, start_month, 1)
        end = NepaliDate(end_year, end_month, 1).end_of_month()

        return {"start": start, "end": end}

    # -------------------------------------------------------------------------
    # Get Current Fiscal Year Quarter
    # -------------------------------------------------------------------------
    def fiscal_quarter(self) -> int:
        """
        Return the fiscal year quarter number (1-4) for the current date.

        Returns:
            int: Fiscal quarter number.
        """
        month = self.get_month()

        if 3 <= month <= 5:
            return 1
        if 6 <= month <= 8:
            return 2
        if 9 <= month <= 11:
            return 3
        return 4

    # -------------------------------------------------------------------------
    # Get Current Fiscal Year Quarter Dates
    # -------------------------------------------------------------------------
    def fiscal_quarter_dates(self) -> Dict[str, "NepaliDate"]:
        """
        Return the start and end dates of the current fiscal year quarter.

        Returns:
            Dict[str, NepaliDate]: Dictionary with 'start' and 'end' keys.
        """
        current_quarter = self.fiscal_quarter()
        current_fiscal_year = NepaliDate.current_fiscal_year()
        return NepaliDate.get_fiscal_quarter(current_quarter, current_fiscal_year)

    # -------------------------------------------------------------------------
    # Get Fiscal Year Quarters
    # -------------------------------------------------------------------------
    @staticmethod
    def get_fiscal_quarters(fiscal_year: int = None) -> Dict[str, Dict[str, "NepaliDate"]]:
        """
        Return the start and end dates for all four quarters of a fiscal year.

        Args:
            fiscal_year (int, optional): The fiscal year. Defaults to current.

        Returns:
            Dict[str, Dict[str, NepaliDate]]: Dictionary mapping Q1-Q4 to their dates.
        """
        year = fiscal_year or NepaliDate.current_fiscal_year()

        return {
            "Q1": NepaliDate.get_fiscal_quarter(1, year),
            "Q2": NepaliDate.get_fiscal_quarter(2, year),
            "Q3": NepaliDate.get_fiscal_quarter(3, year),
            "Q4": NepaliDate.get_fiscal_quarter(4, year),
        }

    # -------------------------------------------------------------------------
    # Comparison operators — pythonic, enables sorting and direct comparison
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Equal to operator
    # -------------------------------------------------------------------------
    def __eq__(self, other: "NepaliDate") -> bool:
        return self.year == other.year and self.month == other.month and self.day == other.day

    # -------------------------------------------------------------------------
    # Less than operator
    # -------------------------------------------------------------------------
    def __lt__(self, other: "NepaliDate") -> bool:
        return self.timestamp < other.timestamp

    # -------------------------------------------------------------------------
    # Greater than operator
    # -------------------------------------------------------------------------
    def __gt__(self, other: "NepaliDate") -> bool:
        return self.timestamp > other.timestamp

    # -------------------------------------------------------------------------
    # Representation operator
    # -------------------------------------------------------------------------
    def __repr__(self) -> str:
        return f"NepaliDate({self.year}, {self.month}, {self.day})"
