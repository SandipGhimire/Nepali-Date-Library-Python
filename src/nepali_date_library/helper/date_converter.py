from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, Type

if TYPE_CHECKING:
    from nepali_date_library import NepaliDate


def ADtoBS(adDate: str, date_class: Optional[Type["NepaliDate"]] = None) -> str:
    """
    Convert a Gregorian (AD) date string to a Nepali Bikram Sambat (BS) date.

    The function expects the input date in ISO format `YYYY-MM-DD`.
    It validates the format, converts the Gregorian date into a `datetime`
    object, and then uses the `NepaliDate` class to perform the conversion.

    Args:
        adDate (str):
            Gregorian date string in the format `"YYYY-MM-DD"`.
        date_class (Type[NepaliDate], optional):
            A `NepaliDate` subclass whose calendar data should be used.
            Defaults to the bundled calendar.

    Raises:
        ValueError:
            - If the input format is invalid.
            - If the date cannot be parsed as a valid Gregorian date.
            - If the conversion to Nepali date fails.

    Returns:
        str:
            Nepali date formatted as `"YYYY-MM-DD"`.

    Example:
        >>> ADtoBS("2023-04-14")
        '2080-01-01'
    """

    import re

    # Validate date format
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", adDate):
        raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")

    year, month, day = map(int, adDate.split("-"))

    try:
        ad = datetime(year, month, day, tzinfo=timezone.utc)
    except ValueError:
        raise ValueError(f"Invalid date input '{adDate}'")

    from nepali_date_library import NepaliDate

    cls = date_class if date_class is not None else NepaliDate

    try:
        nd = cls(ad)
        return nd.format("YYYY-MM-DD")
    except Exception as e:
        raise ValueError(f"Fail to convert AD to BS, Error Detail: {str(e)}")


def BStoAD(bsDate: str, date_class: Optional[Type["NepaliDate"]] = None) -> str:
    """
    Convert a Nepali Bikram Sambat (BS) date string to a Gregorian (AD) date.

    The function expects a Nepali date in ISO format `YYYY-MM-DD`.
    It creates a `NepaliDate` instance and retrieves the internally
    stored Gregorian datetime equivalent.

    Args:
        bsDate (str):
            Nepali date string in the format `"YYYY-MM-DD"`.
        date_class (Type[NepaliDate], optional):
            A `NepaliDate` subclass whose calendar data should be used.
            Defaults to the bundled calendar.

    Raises:
        ValueError:
            - If the input format is invalid.
            - If the Nepali date cannot be parsed.
            - If the conversion to Gregorian date fails.

    Returns:
        str:
            Gregorian date formatted as `"YYYY-MM-DD"`.

    Example:
        >>> BStoAD("2080-01-01")
        '2023-04-14'
    """

    import re

    # Validate date format
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", bsDate):
        raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")

    from nepali_date_library import NepaliDate

    cls = date_class if date_class is not None else NepaliDate

    try:
        nepali_date_instance = cls(bsDate)
        english_date = nepali_date_instance.get_english_date().strftime("%Y-%m-%d")
        return english_date
    except Exception as e:
        raise ValueError(f"Fail to convert BS to AD, Error Detail: {str(e)}")
