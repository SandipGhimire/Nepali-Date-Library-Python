from types import MappingProxyType
from typing import Any, Dict, List, Mapping, Optional, Sequence

from .constants import BUNDLED_CONSTANTS
from .nepali_constants import (
    NepaliConstants,
    NepaliDateMapEntry,
    ProcessedDateMapEntry,
    ProcessedNepaliConstants,
)

_MS_PER_DAY = 86_400_000
_MAX_DAYS_IN_MONTH = 32

_CONSTANT_KEYS = (
    "dateMap",
    "epoch",
    "utcOffsetMs",
    "weekEn",
    "weekShortEn",
    "weekNp",
    "weekShortNp",
    "monthEn",
    "monthShortEn",
    "monthNp",
    "monthShortNp",
    "numberNp",
)

# Required length of every name table.
_NAME_TABLE_SIZES = (
    ("weekEn", 7),
    ("weekShortEn", 7),
    ("weekNp", 7),
    ("weekShortNp", 7),
    ("monthEn", 12),
    ("monthShortEn", 12),
    ("monthNp", 12),
    ("monthShortNp", 12),
    ("numberNp", 10),
)


def _fail(message: str) -> None:
    raise ValueError(f"Invalid Nepali constants: {message}")


def _is_int(value: Any) -> bool:
    # bool is a subclass of int; True/False are never a sensible year or length.
    return isinstance(value, int) and not isinstance(value, bool)


def _is_sequence(value: Any) -> bool:
    return isinstance(value, (list, tuple))


def validate_constants(constants: Mapping[str, Any]) -> None:
    """
    Validate a (raw) constants mapping and raise ``ValueError`` on the first problem found.

    Checks that:

    - every key is present (use :func:`define_constants` to fill gaps from the bundled data)
    - ``dateMap`` is a non-empty list of consecutive years, each with 12 integer month
      lengths (1-32)
    - ``epoch`` is an integer number of milliseconds falling exactly on a UTC midnight
    - ``utcOffsetMs`` is a finite number
    - every name table (weeks, months, digits) has the right size and only holds strings

    Args:
        constants: Constants to validate.

    Raises:
        ValueError: When the constants are not usable.
    """
    if not isinstance(constants, Mapping):
        _fail("constants must be a mapping")

    missing = [key for key in _CONSTANT_KEYS if key not in constants]
    if missing:
        _fail(
            f"missing {', '.join(repr(k) for k in missing)} "
            "(use define_constants() to fill the rest from the bundled data)"
        )

    date_map = constants["dateMap"]
    if not _is_sequence(date_map) or len(date_map) == 0:
        _fail("dateMap must be a non-empty list")

    first_year: Optional[int] = None
    for i, entry in enumerate(date_map):
        if not isinstance(entry, Mapping) or not _is_int(entry.get("year")):
            _fail(f"dateMap[{i}].year must be an integer")
        year = entry["year"]
        if first_year is None:
            first_year = year
        if year != first_year + i:
            expected = first_year + i
            _fail(
                f"dateMap years must be consecutive, expected {expected} "
                f"at index {i} but got {year}"
            )
        days = entry.get("days")
        if not _is_sequence(days) or len(days) != 12:
            _fail(f"dateMap[{i}] (year {year}) must have exactly 12 month lengths")
        for m, month_days in enumerate(days):
            if not _is_int(month_days) or not 1 <= month_days <= _MAX_DAYS_IN_MONTH:
                _fail(
                    f"month {m + 1} of year {year} must be an integer "
                    f"between 1 and {_MAX_DAYS_IN_MONTH}"
                )

    epoch = constants["epoch"]
    if not _is_int(epoch) or epoch % _MS_PER_DAY != 0:
        _fail(
            "epoch must be an integer number of milliseconds on a UTC midnight boundary"
        )

    offset = constants["utcOffsetMs"]
    if (
        isinstance(offset, bool)
        or not isinstance(offset, (int, float))
        or offset != offset  # NaN
        or offset in (float("inf"), float("-inf"))
    ):
        _fail("utcOffsetMs must be a finite number")

    for key, size in _NAME_TABLE_SIZES:
        table = constants[key]
        if not _is_sequence(table) or len(table) != size:
            _fail(f"{key} must be a list of exactly {size} strings")
        if not all(isinstance(item, str) for item in table):
            _fail(f"{key} must only contain strings")


def process_date_map(
    date_map: Sequence[NepaliDateMapEntry],
) -> Sequence[ProcessedDateMapEntry]:
    """
    Build the processed (cumulative) calendar table from a raw one.

    The result is a read-only snapshot: it never shares lists with the input.

    Args:
        date_map: Raw year entries.

    Returns:
        A tuple of read-only year entries with ``totalDays`` and ``daysTillNow`` computed.
    """
    processed: List[Any] = []
    total_days_accumulator = 0

    for entry in date_map:
        days = tuple(entry["days"])
        total_days = sum(days)
        total_days_accumulator += total_days
        processed.append(
            MappingProxyType(
                {
                    "year": entry["year"],
                    "days": days,
                    "totalDays": total_days,
                    "daysTillNow": total_days_accumulator,
                }
            )
        )

    return tuple(processed)


def process_constants(constants: Mapping[str, Any]) -> ProcessedNepaliConstants:
    """
    Validate raw constants and turn them into a read-only, ready-to-use snapshot.

    Later changes to the raw mapping do not affect the snapshot.

    Raises:
        ValueError: When the constants fail validation.
    """
    validate_constants(constants)

    snapshot: Dict[str, Any] = {
        "dateMap": process_date_map(constants["dateMap"]),
        "epoch": constants["epoch"],
        "utcOffsetMs": constants["utcOffsetMs"],
    }
    for key, _ in _NAME_TABLE_SIZES:
        snapshot[key] = tuple(constants[key])

    return MappingProxyType(snapshot)  # type: ignore[return-value]


def find_year_index(date_map: Sequence[Mapping[str, Any]], days_count: int) -> int:
    """
    Find the index of the year block that contains the given zero-based day offset
    (days since the epoch). Binary search, so it works for any year length.

    Args:
        date_map: Processed year entries.
        days_count: Days since the epoch; must be inside the calendar range.
    """
    lo = 0
    hi = len(date_map) - 1

    while lo < hi:
        mid = (lo + hi) >> 1
        if days_count < date_map[mid]["daysTillNow"]:
            hi = mid
        else:
            lo = mid + 1

    return lo


def define_constants(overrides: Optional[NepaliConstants] = None) -> NepaliConstants:
    """
    Build a validated constants dict by layering ``overrides`` over the bundled data.

    Fields that are not overridden fall back to the bundled values, so a partial dict is fine.

    Example:
        >>> year_2101 = {"year": 2101, "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]}
        >>> constants = define_constants({
        ...     "dateMap": [*BUNDLED_CONSTANTS["dateMap"], year_2101],
        ... })

    Args:
        overrides: Any subset of the constants.

    Returns:
        A complete, validated constants dict (a copy, safe to keep).

    Raises:
        ValueError: On unknown keys or invalid values.
    """
    overrides = overrides or {}

    for key in overrides:
        if key not in _CONSTANT_KEYS:
            _fail(f'unknown key "{key}"')

    bundled: Mapping[str, Any] = BUNDLED_CONSTANTS
    given: Mapping[str, Any] = overrides
    merged: Dict[str, Any] = {key: bundled[key] for key in _CONSTANT_KEYS}
    for key in _CONSTANT_KEYS:
        value = given.get(key)
        if value is not None:
            merged[key] = value

    for key in ("epoch", "utcOffsetMs"):
        value = merged[key]
        if isinstance(value, float) and value.is_integer():
            merged[key] = int(value)

    validate_constants(merged)

    result: Dict[str, Any] = {
        "dateMap": [
            {"year": e["year"], "days": list(e["days"])} for e in merged["dateMap"]
        ],
        "epoch": merged["epoch"],
        "utcOffsetMs": merged["utcOffsetMs"],
    }
    for key, _ in _NAME_TABLE_SIZES:
        result[key] = list(merged[key])

    return result  # type: ignore[return-value]
