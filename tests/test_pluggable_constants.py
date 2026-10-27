import pytest
from nepali_date_library import NepaliDate, BUNDLED_CONSTANTS, NepaliConstants


# Custom calendar extending into year 3000-3002
custom_calendar: NepaliConstants = {
    **BUNDLED_CONSTANTS,
    "dateMap": [
        {"year": 3000, "days": [30, 31, 30, 31, 30, 31, 30, 31, 30, 31, 30, 31]},  # 366 (leap)
        {"year": 3001, "days": [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]},  # 360
        {"year": 3002, "days": [31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31]},  # 372
    ],
    "monthEn": [
        "Custom1",
        "Custom2",
        "Custom3",
        "Custom4",
        "Custom5",
        "Custom6",
        "Custom7",
        "Custom8",
        "Custom9",
        "Custom10",
        "Custom11",
        "Custom12",
    ],
}


class ExtendedNepaliDate(NepaliDate):
    def _get_constants(self) -> NepaliConstants:
        return custom_calendar


def test_constructs_from_string_in_custom_calendar_year_range():
    d = ExtendedNepaliDate("3000-02-15")
    assert d.get_year() == 3000
    assert d.get_month() == 1  # 0-indexed
    assert d.get_date() == 15
    assert d.format("YYYY-MM-DD") == "3000-02-15"


def test_constructs_from_year_month_day_in_custom_range():
    d = ExtendedNepaliDate(3001, 5, 20)
    assert d.get_year() == 3001
    assert d.get_month() == 5
    assert d.get_date() == 20
    assert d.format("YYYY-MM-DD") == "3001-06-20"


def test_throws_when_string_is_out_of_custom_calendar_range():
    with pytest.raises(ValueError, match="Nepal year out of range"):
        ExtendedNepaliDate("2080-01-01")


def test_throws_when_year_integer_is_out_of_custom_calendar_range():
    with pytest.raises(ValueError, match="Nepal year out of range"):
        ExtendedNepaliDate(2080, 0, 1)


def test_throws_when_day_exceeds_custom_month_day_limit():
    # In year 3001, month 1 (index 0) has 30 days
    with pytest.raises(ValueError, match="Invalid Nepali date"):
        ExtendedNepaliDate("3001-01-31")


def test_computes_days_in_month_correctly_from_custom_data():
    d = ExtendedNepaliDate("3000-01-01")
    assert d.days_in_month() == 30
    d_m2 = ExtendedNepaliDate("3000-02-01")
    assert d_m2.days_in_month() == 31


def test_evaluates_is_leap_year_based_on_custom_total_days():
    leap = ExtendedNepaliDate("3000-01-01")
    assert leap.is_leap_year() is True  # 366 days

    non_leap = ExtendedNepaliDate("3001-01-01")
    assert non_leap.is_leap_year() is False  # 360 days


def test_correctly_validates_dates_with_is_valid_instance():
    valid = ExtendedNepaliDate("3000-01-10")
    assert valid.is_valid_instance() is True

    invalid_day = ExtendedNepaliDate("3000-01-30")
    invalid_day.day = 32
    assert invalid_day.is_valid_instance() is False


def test_adds_months_and_preserves_subclass():
    d = ExtendedNepaliDate("3000-01-15")
    next_month = d.add_months(2)

    assert isinstance(next_month, ExtendedNepaliDate)
    assert next_month.format("YYYY-MM-DD") == "3000-03-15"


def test_adds_years_and_preserves_subclass():
    d = ExtendedNepaliDate("3000-05-10")
    next_year = d.add_years(1)

    assert isinstance(next_year, ExtendedNepaliDate)
    assert next_year.format("YYYY-MM-DD") == "3001-05-10"


def test_adds_days_and_preserves_subclass():
    d = ExtendedNepaliDate("3000-01-01")
    next_day = d.add_days(5)

    assert isinstance(next_day, ExtendedNepaliDate)
    assert next_day.format("YYYY-MM-DD") == "3000-01-06"


def test_clamps_day_when_adding_months_to_a_month_with_fewer_days():
    # 3000-02 has 31 days, but 3000-03 (index 2) has 30 days
    d = ExtendedNepaliDate("3000-02-31")
    next_month = d.add_months(1)

    assert next_month.format("YYYY-MM-DD") == "3000-03-30"


def test_computes_end_of_year_according_to_custom_last_month_days():
    d = ExtendedNepaliDate("3000-01-01")
    end = d.end_of_year()

    assert isinstance(end, ExtendedNepaliDate)
    # month 12 (index 11) has 31 days in year 3000
    assert end.format("YYYY-MM-DD") == "3000-12-31"


def test_formats_with_custom_month_names():
    d = ExtendedNepaliDate("3000-01-01")
    assert d.format("MMMM YYYY") == "Custom1 3000"

    d2 = ExtendedNepaliDate("3000-05-01")
    assert d2.format("MMMM") == "Custom5"


def test_detects_when_custom_constants_reference_updates():
    current_data = {**custom_calendar}

    class DynamicNepaliDate(NepaliDate):
        def _get_constants(self) -> NepaliConstants:
            return current_data

    d = DynamicNepaliDate("3000-01-01")
    assert d.days_in_month() == 30

    # Simulate runtime update
    current_data = {
        **custom_calendar,
        "dateMap": [
            {"year": 3000, "days": [32, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]},
            *custom_calendar["dateMap"][1:],
        ],
    }

    # Same instance dynamically reflects updated constants
    assert d.days_in_month() == 32

