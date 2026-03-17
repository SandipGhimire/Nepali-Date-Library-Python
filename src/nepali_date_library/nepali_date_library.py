from datetime import datetime, timezone, timedelta
from typing import Tuple, Union, Dict, List
from .helper.constants import nepali_date_map, EPOCH, month_short_np, month_np, month_short_en, month_en
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

    def parse(self, date_string: str) -> None:
        self.set(*_parse(date_string))

    def get_year(self) -> int:
        return self.year

    def get_month(self) -> int:
        return self.month

    def get_day(self) -> int:
        return self.timestamp.weekday()

    def get_date(self) -> int:
        return self.day

    def set_year(self, year: int) -> None:
        self.set(year, self.month, self.day)

    def set_month(self, month: int) -> None:
        self.set(self.year, month, self.day)

    def set_date(self, day: int) -> None:
        self.set(self.year, self.month, day)

    def add_days(self, days: int) -> 'NepaliDate':
        new_timestamp = self.timestamp + timedelta(days=days)
        return NepaliDate(new_timestamp)

    def add_months(self, months: int) -> 'NepaliDate':
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

    def add_years(self, years: int) -> 'NepaliDate':
        new_year = self.year + years

        if new_year < nepali_date_map[0]["year"] or new_year >= nepali_date_map[0]["year"] + len(nepali_date_map):
            raise ValueError("Resulting date is out of supported range")

        year_index = new_year - nepali_date_map[0]["year"]

        days_in_new_year_month = nepali_date_map[year_index]["days"][self.month]
        new_day = min(self.day, days_in_new_year_month)

        return NepaliDate(new_year, self.month, new_day)

    @staticmethod
    def minimum() -> datetime:
        return datetime.fromtimestamp(EPOCH / 1000, tz=timezone.utc)

    @staticmethod
    def maximum() -> datetime:
        return datetime.fromtimestamp((EPOCH + (nepali_date_map[-1]["daysTillNow"] * 86400000)) / 1000, tz=timezone.utc)

    def days_in_month(self) -> int:
        year_index = self.year - nepali_date_map[0]["year"]
        return nepali_date_map[year_index]["days"][self.month]

    def is_leap_year(self) -> bool:
        year_index = self.year - nepali_date_map[0]["year"]
        print(nepali_date_map[year_index]["totalDays"])
        return nepali_date_map[year_index]["totalDays"] >= 366

    def getWeeksInMonth(self) -> int:
        first_day = NepaliDate(self.year, self.month, 1)
        first_day_of_week = first_day.get_day()
        total_days = self.days_in_month()
        return math.ceil((total_days + first_day_of_week) / 7)

    def diff(self, date: "NepaliDate", unit: str) -> int:
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

    def start_of_day(self) -> "NepaliDate":
        start = self.timestamp.replace(
            hour=0, minute=0, second=0, microsecond=0)
        return NepaliDate(start)

    def end_of_day(self) -> "NepaliDate":
        end = self.timestamp.replace(
            hour=23, minute=59, second=59, microsecond=999000)
        return NepaliDate(end)

    def start_of_week(self, start_of_week: int = 0) -> "NepaliDate":
        if start_of_week < 0 or start_of_week > 6:
            raise ValueError(
                "start_of_week mush be an integer between 0 and 6")

        current_day = self.get_day()
        day_to_subtract = (current_day - start_of_week + 7) % 7
        result = self.clone().start_of_day()
        result.add_days(-day_to_subtract)
        return result

    def end_of_week(self, start_of_week: int = 0) -> "NepaliDate":
        if start_of_week < 0 or start_of_week > 6:
            raise ValueError(
                "start_of_week mush be an integer between 0 and 6")

        start_of_week = self.start_of_week(start_of_week)
        return start_of_week.add_days(6).end_of_day()

    def start_of_month(self) -> "NepaliDate":
        return NepaliDate(self.year, self.month, 1).start_of_day()

    def end_of_month(self) -> "NepaliDate":
        return NepaliDate(self.year, self.month, self.days_in_month()).end_of_day()

    def start_of_year(self) -> "NepaliDate":
        return NepaliDate(self.year, 0, 1).start_of_day()

    def end_of_year(self) -> "NepaliDate":
        return NepaliDate(self.year, 11, self.days_in_month()).end_of_day()

    @staticmethod
    def get_month_name(month: int, short: bool = False, nepali: bool = False) -> str:
        if month < 0 or month > 11:
            raise ValueError("Invalid month index, must be between 0-11")

        result = ""
        if nepali:
            result = month_short_np[month] if short else month_np[month]
        else:
            result = month_short_en[month] if short else month_en[month]

        return result

    @staticmethod
    def get_day_name(day, short: bool = False, nepali: bool = False) -> str:
        if day < 0 or day > 6:
            raise ValueError("Invalid day index, must be between 0-6")

        if nepali:
            result = day_short_np[day] if short else day_np[day]
        else:
            result = day_short_en[day] if short else day_en[day]

        return result

    @staticmethod
    def is_valid(year: int, month: int, date: int) -> bool:
        if year < nepali_date_map[0]["year"] or year >= nepali_date_map[0]["year"] + len(nepali_date_map):
            return False

        if month < 0 or month > 11:
            return False

        year_index = year - nepali_date_map[0]["year"]
        days_in_month = nepali_date_map[year_index]["days"][month]

        if date < 1 or date > days_in_month:
            return False

        return True

    def is_current_valid(self) -> bool:
        return NepaliDate.is_valid(self.year, self.month, self.day)

    def is_after(self, date: "NepaliDate") -> bool:
        return self.timestamp > date.timestamp

    def is_before(self, date: "NepaliDate") -> bool:
        return self.timestamp < date.timestamp

    def is_equal(self, date: "NepaliDate") -> bool:
        return self.timestamp == date.timestamp

    def is_same(self, date: "NepaliDate", unit: str) -> bool:
        if unit == "year":
            return self.year == date.year
        elif unit == "month":
            return self.year == date.year and self.month == date.month
        elif unit == "day":
            return self.is_equal(date)
        else:
            raise ValueError("Invalid unit for same check")

    def get_quarter(self, quarter: int) -> Dict[str, "NepaliDate"]:
        if quarter < 1 or quarter > 4:
            raise ValueError("Invalid quarter, must be between 1-4")

        return NepaliDate.get_quarter_by_year(quarter, self.year)

    @staticmethod
    def get_quarter_by_year(quarter: int, year: int) -> Dict[str, "NepaliDate"]:
        if quarter < 1 or quarter > 4:
            raise ValueError("Invalid quarter, must be between 1-4")
        if nepali_date_map[year - nepali_date_map[0]["year"]] == None:
            raise ValueError("Invalid year")

        nepali_year = year
        start_month = (quarter - 1) * 3

        start = NepaliDate(nepali_year, start_month, 1)
        end = start.add_months(2).end_of_month()

        return {"start": start, "end": end}

    def get_current_quarter(self) -> int:
        return self.month // 3 + 1

    def get_quarters(self) -> List[Dict[str, "NepaliDate"]]:
        return NepaliDate.get_quarters_by_year(self.year)

    @staticmethod
    def get_quarters_by_year(year) -> List[Dict[str, "NepaliDate"]]:
        if nepali_date_map[year - nepali_date_map[0]["year"]] == None:
            raise ValueError("Invalid year")

        nepali_year = year

        return {
            "Q1": NepaliDate.get_quarter_by_year(1, year),
            "Q2": NepaliDate.get_quarter_by_year(2, year),
            "Q3": NepaliDate.get_quarter_by_year(3, year),
            "Q4": NepaliDate.get_quarter_by_year(4, year)
        }

    @staticmethod
    def get_current_fiscal_year() -> int:
        today = NepaliDate()
        year = today.get_year()
        month = today.get_month()
        return year - 1 if month < 3 else year

    @staticmethod
    def get_fiscal_year_quarter(quarter: int, fiscal_year: int = None) -> Dict[str, "NepaliDate"]:
        if quarter < 1 or quarter > 4 or not isinstance(quarter, int):
            raise ValueError("Quarter must be an integer between 1 and 4")

        current_fiscal_year = fiscal_year or NepaliDate.get_current_fiscal_year()

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

    def get_current_fiscal_year_quarter(self) -> int:
        month = self.get_month()

        if 3 <= month <= 5:
            return 1
        if 6 <= month <= 8:
            return 2
        if 9 <= month <= 11:
            return 3
        return 4

    def get_current_fiscal_year_quarter_dates(self) -> Dict[str, "NepaliDate"]:
        current_quarter = self.get_current_fiscal_year_quarter()
        current_fiscal_year = NepaliDate.get_current_fiscal_year()
        return NepaliDate.get_fiscal_year_quarter(current_quarter, current_fiscal_year)

    @staticmethod
    def get_fiscal_year_quarters(fiscal_year: int = None) -> Dict[str, Dict[str, "NepaliDate"]]:
        year = fiscal_year or NepaliDate.get_current_fiscal_year()

        return {
            "Q1": NepaliDate.get_fiscal_year_quarter(1, year),
            "Q2": NepaliDate.get_fiscal_year_quarter(2, year),
            "Q3": NepaliDate.get_fiscal_year_quarter(3, year),
            "Q4": NepaliDate.get_fiscal_year_quarter(4, year),
        }
