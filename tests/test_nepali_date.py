from datetime import datetime, timezone

import pytest

from nepali_date_library import NepaliDate, nepali_date_map


# -------------------------------------------------------------------
# Construction
# -------------------------------------------------------------------
def test_construct_with_year_month_day():
    d = NepaliDate(2080, 0, 15)
    assert d.get_year() == 2080
    assert d.get_month() == 0
    assert d.get_date() == 15
    assert d.format("YYYY-MM-DD") == "2080-01-15"


def test_construct_from_datetime():
    ad = datetime(2023, 4, 28, tzinfo=timezone.utc)
    d = NepaliDate(ad)
    assert d.format("YYYY-MM-DD") == "2080-01-15"


def test_construct_from_nepali_date_copies_state():
    original = NepaliDate(2080, 5, 10)
    copy = NepaliDate(original)

    assert copy.get_year() == original.get_year()
    assert copy.get_month() == original.get_month()
    assert copy.get_date() == original.get_date()
    assert copy.get_time() == original.get_time()


@pytest.mark.parametrize(
    "input_str",
    ["2080-01-01", "2080/1/1", "2080.1.1", "2080"],
    ids=["dashes", "slashes", "dots", "year-only-defaults-month-day-to-1"],
)
def test_construct_from_string(input_str):
    d = NepaliDate(input_str)
    assert d.format("YYYY-MM-DD") == "2080-01-01"


def test_construct_from_epoch_millisecond_timestamp():
    from nepali_date_library.helper.constants import EPOCH

    d = NepaliDate(EPOCH)
    assert d.format("YYYY-MM-DD") == "1976-01-01"


def test_construct_with_no_arguments_gives_a_valid_current_date():
    d = NepaliDate()
    assert d.is_valid_instance() is True


def test_construct_raises_on_invalid_argument_type():
    with pytest.raises(ValueError, match="Invalid argument syntax"):
        NepaliDate(3.14)  # type: ignore[arg-type]


def test_construct_raises_on_invalid_date_string():
    with pytest.raises(ValueError):
        NepaliDate("not-a-date")


def test_construct_raises_on_year_out_of_range():
    with pytest.raises(ValueError, match="Nepal year out of range"):
        NepaliDate("1975-01-01")


def test_construct_raises_on_invalid_month():
    with pytest.raises(ValueError, match="Invalid Nepali month must be between 1 - 12"):
        NepaliDate("2080-13-01")


def test_construct_raises_on_invalid_day():
    with pytest.raises(ValueError):
        NepaliDate("2080-01-32")


def test_set_raises_with_exclamation_message_on_year_out_of_range():
    d = NepaliDate(2080, 0, 1)
    with pytest.raises(ValueError, match=r"Nepal year out of range!"):
        d.set(1800, 0, 1)


# -------------------------------------------------------------------
# Formatting
# -------------------------------------------------------------------
def test_format_english_tokens():
    d = NepaliDate(2080, 0, 15)

    assert d.format("YYYY") == "2080"
    assert d.format("YYY") == "080"
    assert d.format("YY") == "80"

    assert d.format("M") == "1"
    assert d.format("MM") == "01"
    assert d.format("MMM") == "Bai"
    assert d.format("MMMM") == "Baisakh"

    assert d.format("D") == "15"
    assert d.format("DD") == "15"
    assert d.format("DDD") == "Fri"
    assert d.format("DDDD") == "Friday"


def test_format_nepali_tokens():
    d = NepaliDate(2080, 0, 15)

    assert d.format("yyyy") == "२०८०"
    assert d.format("m") == "१"
    assert d.format("mm") == "०१"
    assert d.format("mmm") == "बै"
    assert d.format("mmmm") == "बैशाख"
    assert d.format("dd") == "१५"
    assert d.format("ddd") == "शुक्र"
    assert d.format("dddd") == "शुक्रबार"


def test_format_with_quoted_literals():
    d = NepaliDate(2080, 0, 15)
    assert d.format('"M"MM') == "M01"


def test_str_matches_format_of_y_m_d():
    d = NepaliDate(2080, 0, 5)
    assert str(d) == "2080/1/5"


# -------------------------------------------------------------------
# Arithmetic
# -------------------------------------------------------------------
def test_add_days_rolls_into_next_month():
    d = NepaliDate(2080, 0, 31)  # Baisakh 2080 has 31 days
    assert d.add_days(1).format("YYYY-MM-DD") == "2080-02-01"


def test_add_months_within_year():
    d = NepaliDate(2080, 0, 15)
    next_ = d.add_months(1)
    assert next_.get_year() == 2080
    assert next_.get_month() == 1


def test_add_months_does_not_double_count_year_on_negative_rollover():
    """
    Regression test mirroring NodeJS/PHP: -1 month from Baisakh must land in
    the previous year's Chaitra without double-decrementing the year.
    """
    start = NepaliDate(2080, 0, 15)

    back1 = start.add_months(-1)
    assert back1.get_year() == 2079
    assert back1.get_month() == 11

    back13 = start.add_months(-13)
    assert back13.get_year() == 2078
    assert back13.get_month() == 11

    back12 = start.add_months(-12)
    assert back12.get_year() == 2079
    assert back12.get_month() == 0


def test_add_years_caps_day_to_target_month_length():
    d = NepaliDate(2084, 10, 30)  # Falgun 30, 2084
    next_ = d.add_years(1)
    assert next_.format("YYYY-MM-DD") == "2085-11-29"  # 2085's Falgun only has 29 days


def test_set_year_month_date():
    d = NepaliDate(2080, 0, 15)

    d.set_year(2081)
    assert d.get_year() == 2081

    d.set_month(5)
    assert d.get_month() == 5

    d.set_date(20)
    assert d.get_date() == 20


# -------------------------------------------------------------------
# Calendar metadata
# -------------------------------------------------------------------
def test_days_in_month_and_leap_year():
    d = NepaliDate(2080, 0, 15)
    assert d.days_in_month() == 31
    assert d.is_leap_year() is False


def test_get_weeks_in_month():
    d = NepaliDate(2080, 0, 15)
    assert d.get_weeks_in_month() == 6


def test_minimum_and_maximum():
    assert NepaliDate.minimum().strftime("%Y-%m-%d") == "1919-04-13"

    last = nepali_date_map[-1]
    expected_max_ad = (
        NepaliDate(last["year"], 11, last["days"][11]).get_english_date().strftime("%Y-%m-%d")
    )
    assert NepaliDate.maximum().strftime("%Y-%m-%d") == expected_max_ad


def test_maximum_round_trips_back_into_a_valid_nepali_date():
    """
    Regression test: maximum() used to return a date one day past the actual
    last supported day (daysTillNow is a 1-indexed count), which meant
    round-tripping it back into a NepaliDate would raise.
    """
    max_date = NepaliDate(NepaliDate.maximum())
    last = nepali_date_map[-1]

    assert max_date.get_year() == last["year"]
    assert max_date.get_month() == 11
    assert max_date.get_date() == last["days"][11]
    assert max_date.is_valid_instance() is True


# -------------------------------------------------------------------
# Time getters
# -------------------------------------------------------------------
def test_time_getters():
    ad = datetime(2023, 4, 28, 13, 45, 30, 250000, tzinfo=timezone.utc)
    d = NepaliDate(ad)

    assert d.get_hours() == 13
    assert d.get_minutes() == 45
    assert d.get_seconds() == 30
    assert d.get_milliseconds() == 250
    assert d.get_time() == int(ad.timestamp() * 1000)


def test_get_day_is_sunday_indexed():
    """
    Regression test: get_day() used to be Monday-indexed (raw
    datetime.weekday()), which mismatched week_en/week_np (Sunday-indexed)
    and produced wrong weekday names in format().
    """
    d = NepaliDate(2080, 0, 15)  # Friday
    assert d.get_day() == 5
    assert d.get_day_name(d.get_day()) == "Friday"


# -------------------------------------------------------------------
# Start/end of day/week/month/year
# -------------------------------------------------------------------
def test_start_and_end_of_day():
    d = NepaliDate(2080, 0, 15)

    assert d.start_of_day().get_english_date().strftime("%Y-%m-%dT%H:%M:%S") == "2023-04-28T00:00:00"
    assert d.end_of_day().get_english_date().strftime("%Y-%m-%dT%H:%M:%S") == "2023-04-28T23:59:59"
    assert d.end_of_day().get_milliseconds() == 999


def test_start_and_end_of_week():
    d = NepaliDate(2080, 0, 15)  # Friday

    assert d.start_of_week().format("YYYY-MM-DD") == "2080-01-10"
    assert d.start_of_week().get_day() == 0
    assert d.end_of_week().format("YYYY-MM-DD") == "2080-01-16"


def test_start_of_week_rejects_out_of_range_argument():
    d = NepaliDate(2080, 0, 15)
    with pytest.raises(ValueError):
        d.start_of_week(7)


def test_start_and_end_of_month():
    d = NepaliDate(2080, 0, 15)
    assert d.start_of_month().format("YYYY-MM-DD") == "2080-01-01"
    assert d.end_of_month().format("YYYY-MM-DD") == "2080-01-31"


def test_start_and_end_of_year():
    d = NepaliDate(2080, 0, 15)
    assert d.start_of_year().format("YYYY-MM-DD") == "2080-01-01"
    assert d.end_of_year().format("YYYY-MM-DD") == "2080-12-30"


# -------------------------------------------------------------------
# Comparisons and diff
# -------------------------------------------------------------------
def test_comparisons():
    a = NepaliDate(2080, 0, 1)
    b = NepaliDate(2080, 0, 15)
    c = NepaliDate(2080, 0, 1)

    assert b.is_after(a) is True
    assert a.is_before(b) is True
    assert a.is_equal(c) is True
    assert a.is_equal(b) is False


def test_is_same():
    a = NepaliDate(2080, 5, 10)
    b = NepaliDate(2080, 5, 20)
    c = NepaliDate(2081, 5, 10)

    assert a.is_same(b, "year") is True
    assert a.is_same(b, "month") is True
    assert a.is_same(b, "day") is False
    assert a.is_same(c, "year") is False


def test_diff():
    a = NepaliDate(2080, 5, 10)
    b = NepaliDate(2080, 0, 10)

    assert a.diff(b, "month") == 5
    assert a.diff(b, "year") == 0
    assert a.diff(b, "day") > 0


def test_diff_raises_on_invalid_unit():
    a = NepaliDate(2080, 5, 10)
    b = NepaliDate(2080, 0, 10)

    with pytest.raises(ValueError):
        a.diff(b, "week")


# -------------------------------------------------------------------
# Quarters and fiscal years
# -------------------------------------------------------------------
def test_get_quarter():
    q1 = NepaliDate.get_quarter(1, 2080)
    assert q1["start"].format("YYYY-MM-DD") == "2080-01-01"
    assert q1["end"].format("YYYY-MM-DD") == "2080-03-31"

    q4 = NepaliDate.get_quarter(4, 2080)
    assert q4["start"].format("YYYY-MM-DD") == "2080-10-01"
    assert q4["end"].format("YYYY-MM-DD") == "2080-12-30"


def test_get_quarter_rejects_out_of_range():
    with pytest.raises(ValueError):
        NepaliDate.get_quarter(5, 2080)


def test_get_quarters():
    quarters = NepaliDate.get_quarters(2080)
    assert list(quarters.keys()) == ["Q1", "Q2", "Q3", "Q4"]
    assert quarters["Q1"]["start"].format("YYYY-MM-DD") == "2080-01-01"


def test_current_quarter():
    d = NepaliDate(2080, 0, 15)
    assert d.current_quarter() == 1


def test_get_fiscal_quarter():
    fq1 = NepaliDate.get_fiscal_quarter(1, 2080)
    assert fq1["start"].format("YYYY-MM-DD") == "2080-04-01"
    assert fq1["end"].format("YYYY-MM-DD") == "2080-06-30"

    fq4 = NepaliDate.get_fiscal_quarter(4, 2080)
    assert fq4["start"].format("YYYY-MM-DD") == "2081-01-01"
    assert fq4["end"].format("YYYY-MM-DD") == "2081-03-31"


def test_fiscal_quarter():
    d = NepaliDate(2080, 0, 15)  # Baisakh -> fiscal Q4
    assert d.fiscal_quarter() == 4

    d2 = NepaliDate(2080, 3, 15)  # Shrawan -> fiscal Q1
    assert d2.fiscal_quarter() == 1


def test_get_fiscal_quarters():
    quarters = NepaliDate.get_fiscal_quarters(2080)
    assert list(quarters.keys()) == ["Q1", "Q2", "Q3", "Q4"]


# -------------------------------------------------------------------
# Static helpers
# -------------------------------------------------------------------
def test_get_month_name():
    assert NepaliDate.get_month_name(0) == "Baisakh"
    assert NepaliDate.get_month_name(0, True) == "Bai"
    assert NepaliDate.get_month_name(0, False, True) == "बैशाख"
    assert NepaliDate.get_month_name(0, True, True) == "बै"


def test_get_month_name_rejects_out_of_range():
    with pytest.raises(ValueError):
        NepaliDate.get_month_name(12)


def test_get_day_name():
    assert NepaliDate.get_day_name(0) == "Sunday"
    assert NepaliDate.get_day_name(0, True) == "Sun"
    assert NepaliDate.get_day_name(0, False, True) == "आइतबार"
    assert NepaliDate.get_day_name(0, True, True) == "आइत"


def test_is_valid_static_and_instance():
    assert NepaliDate.is_valid(2080, 0, 31) is True
    assert NepaliDate.is_valid(2080, 0, 32) is False
    assert NepaliDate.is_valid(1800, 0, 1) is False

    d = NepaliDate(2080, 0, 15)
    assert d.is_valid_instance() is True


def test_get_calendar_days_structure():
    cal = NepaliDate.get_calendar_days(2080, 0)

    assert cal["prev_remaining_days"] == 5
    assert cal["remaining_days"] == 6
    assert cal["prev_month"] == {"year": 2079, "month": 11, "days": [26, 27, 28, 29, 30]}
    assert cal["next_month"] == {"year": 2080, "month": 1, "days": [1, 2, 3, 4, 5, 6]}
    assert len(cal["current_month"]["days"]) == 31


def test_get_calendar_days_rejects_invalid_month():
    with pytest.raises(ValueError):
        NepaliDate.get_calendar_days(2080, 12)
