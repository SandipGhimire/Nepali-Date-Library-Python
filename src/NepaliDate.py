from datetime import datetime, timezone
from typing import Tuple, Union
from Helper import NEPALI_DATE_MAP, EPOCH, format_date


def _parse(date_string: str) -> Tuple[int, int, int]:
    """
    Parses a Nepali date string into components (year, month, day)
    Month returned is 0-indexed.
    """
    import re

    parts = re.split(r"[-./]", date_string, maxsplit=2)
    try:
        year = int(parts[0])
        month = int(parts[1]) if len(parts) > 1 else 1
        day = int(parts[2]) if len(parts) > 2 else 1
    except ValueError:
        raise ValueError("Invalid date")

    if year < NEPALI_DATE_MAP[0]["year"] or year >= NEPALI_DATE_MAP[0]["year"] + len(NEPALI_DATE_MAP):
        raise ValueError("Nepal year out of range")

    if month < 1 or month > 12:
        raise ValueError("Invalid Nepali month must be between 1 - 12")

    days_in_month = NEPALI_DATE_MAP[year -
                                    NEPALI_DATE_MAP[0]["year"]]["days"][month - 1]
    if day < 1 or day > days_in_month:
        raise ValueError(
            f"Invalid Nepali date must be between 1 - {days_in_month} in {year}-{month}")

    return year, month - 1, day


class NepaliDate:
    def __init__(self, year_or_date: Union[datetime, 'NepaliDate', int, str] = None,
                 month: int = None, day: int = None):
        self.timestamp: datetime = None
        self.year: int = None
        self.month: int = None
        self.day: int = None

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
            self.set_english_date(datetime.fromtimestamp(year_or_date / 1000))
        else:
            raise ValueError("Invalid argument syntax")

    def set_english_date(self, date: datetime):
        """
        Sets internal Nepali date from Gregorian date.
        """
        self.timestamp = date

        utc_time = int(datetime(date.year, date.month, date.day,
                       tzinfo=timezone.utc).timestamp() * 1000)
        days_count = (utc_time - EPOCH) // 86400000
        idx = days_count // 366

        while days_count >= NEPALI_DATE_MAP[idx]["daysTillNow"]:
            idx += 1

        prev_till_now = NEPALI_DATE_MAP[idx -
                                        1]["daysTillNow"] if idx - 1 >= 0 else 0
        days_count -= prev_till_now

        tmp = NEPALI_DATE_MAP[idx]
        self.year = tmp["year"]
        self.month = 0

        while days_count >= tmp["days"][self.month]:
            days_count -= tmp["days"][self.month]
            self.month += 1

        self.day = days_count + 1

    def set(self, year: int, month: int, date: int):
        """
        Sets Nepali date and calculates the equivalent Gregorian date.
        """
        idx = year + (month // 12) - NEPALI_DATE_MAP[0]["year"]
        if idx < 0 or idx >= len(NEPALI_DATE_MAP):
            raise ValueError("Nepal year out of range!")

        tmp = NEPALI_DATE_MAP[idx]
        d = tmp["daysTillNow"] - sum(tmp["days"])

        m = month % 12
        mm = m if m >= 0 else 12 + m

        for i in range(mm):
            d += tmp["days"][i]

        d += date - 1

        utc_timestamp = EPOCH + d * 86400000
        utc_date = datetime.fromtimestamp(
            utc_timestamp / 1000, tz=timezone.utc)

        self.set_english_date(utc_date)

    def format(self, format_str: str) -> str:
        """
        Formats the Nepali date according to the given format string.
        This requires a separate formatter function similar to JS DateFormatter.
        """
        return format_date(self, format_str)

    def __str__(self) -> str:
        """
        Returns Nepali date as 'YYYY/MM/DD', month is 1-indexed.
        """
        return f"{self.year}/{self.month + 1}/{self.day}"
