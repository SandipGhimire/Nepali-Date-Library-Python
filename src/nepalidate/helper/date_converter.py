from datetime import datetime, timezone


def ADtoBS(adDate: str) -> str:
    """
    Convert a Gregorian (AD) date string to a Nepali Bikram Sambat (BS) date.

    The function expects the input date in ISO format `YYYY-MM-DD`.
    It validates the format, converts the Gregorian date into a `datetime`
    object, and then uses the `NepaliDate` class to perform the conversion.

    Args:
        adDate (str):
            Gregorian date string in the format `"YYYY-MM-DD"`.

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

    from nepalidate import NepaliDate

    try:
        nd = NepaliDate(ad)
        return nd.format("YYYY-MM-DD")
    except Exception as e:
        raise ValueError(f"Fail to convert AD to BS, Error Detail: {str(e)}")


def BStoAD(bsDate: str) -> str:
    """
    Convert a Nepali Bikram Sambat (BS) date string to a Gregorian (AD) date.

    The function expects a Nepali date in ISO format `YYYY-MM-DD`.
    It creates a `NepaliDate` instance and retrieves the internally
    stored Gregorian datetime equivalent.

    Args:
        bsDate (str):
            Nepali date string in the format `"YYYY-MM-DD"`.

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

    from nepalidate import NepaliDate

    try:
        nepali_date_instance = NepaliDate(bsDate)
        english_date = nepali_date_instance.get_english_date().strftime("%Y-%m-%d")
        return english_date
    except Exception as e:
        raise ValueError(f"Fail to convert BS to AD, Error Detail: {str(e)}")
