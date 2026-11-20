"""
Tests for custom calendar data: ``define_constants``, ``validate_constants`` and ``NepaliDate``
subclasses that override ``constants()``.
"""

from datetime import datetime, timezone

import pytest

from nepali_date_library import (
    ADtoBS,
    BStoAD,
    BUNDLED_CONSTANTS,
    NepaliDate,
    define_constants,
    validate_constants,
)
from nepali_date_library.helper.utils import find_year_index, process_constants

DAY_MS = 86_400_000
DEFAULT_EPOCH = BUNDLED_CONSTANTS["epoch"]


def names(count, prefix, start=0):
    return [f"{prefix}{i + start}" for i in range(count)]


def ad_of(days_since_epoch, epoch=DEFAULT_EPOCH):
    return datetime.fromtimestamp(
        (epoch + days_since_epoch * DAY_MS) / 1000, tz=timezone.utc
    ).strftime("%Y-%m-%d")


def utc_ms(year, month, day, hour=0, minute=0, second=0, millisecond=0):
    moment = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
    return int(moment.timestamp() * 1000) + millisecond


def utc_dt(year, month, day, hour=0, minute=0, second=0, millisecond=0):
    return datetime(
        year, month, day, hour, minute, second, millisecond * 1000, tzinfo=timezone.utc
    )


def thirty(year):
    return {"year": year, "days": [30] * 12}


def ymd(d):
    return d.format("YYYY-MM-DD")


# 3000 = 366 days, 3001 = 360 days, 3002 = 372 days.
# Years longer than 366 days used to break lookups.
CAL = define_constants(
    {
        "dateMap": [
            {"year": 3000, "days": [30, 31, 30, 31, 30, 31, 30, 31, 30, 31, 30, 31]},
            {"year": 3001, "days": [30] * 12},
            {"year": 3002, "days": [31] * 12},
        ],
        "weekEn": names(7, "Day"),
        "weekShortEn": names(7, "D"),
        "weekNp": names(7, "NpDay"),
        "weekShortNp": names(7, "ND"),
        "monthEn": names(12, "Month", 1),
        "monthShortEn": names(12, "M", 1),
        "monthNp": names(12, "NpMonth", 1),
        "monthShortNp": names(12, "NM", 1),
        "numberNp": list("abcdefghij"),
    }
)


def make_class(constants_obj, name="Custom"):
    """Create a NepaliDate subclass bound to one constants object."""

    class _Date(NepaliDate):
        @classmethod
        def constants(cls):
            return constants_obj

    _Date.__name__ = name
    return _Date


Cal = make_class(CAL, "Cal")

LONG = define_constants(
    {"dateMap": [{"year": y, "days": [31] * 12} for y in range(3000, 3005)]}
)
Long = make_class(LONG, "Long")

EXTRA_YEAR = {"year": 2101, "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]}
EXTENDED = define_constants({"dateMap": [*BUNDLED_CONSTANTS["dateMap"], EXTRA_YEAR]})
Extended = make_class(EXTENDED, "Extended")

CUSTOM_EPOCH = utc_ms(2000, 1, 1)
UTC_CAL = define_constants(
    {"epoch": CUSTOM_EPOCH, "utcOffsetMs": 0, "dateMap": [thirty(1), thirty(2)]}
)
PLUS5_CAL = define_constants(
    {"epoch": CUSTOM_EPOCH, "utcOffsetMs": 5 * 3600000, "dateMap": [thirty(1)]}
)
WEST_CAL = define_constants(
    {"epoch": CUSTOM_EPOCH, "utcOffsetMs": -3 * 3600000, "dateMap": [thirty(1)]}
)
Utc, Plus5, West = (
    make_class(UTC_CAL, "Utc"),
    make_class(PLUS5_CAL, "Plus5"),
    make_class(WEST_CAL, "West"),
)


# ----------------------------------------------------------------------------------------------
# define_constants
# ----------------------------------------------------------------------------------------------
class TestDefineConstants:
    def test_no_overrides_returns_a_complete_copy_of_the_bundled_data(self):
        c = define_constants()
        assert c["epoch"] == BUNDLED_CONSTANTS["epoch"]
        assert c["utcOffsetMs"] == BUNDLED_CONSTANTS["utcOffsetMs"]
        assert c["monthEn"] == list(BUNDLED_CONSTANTS["monthEn"])
        assert c["numberNp"] == list(BUNDLED_CONSTANTS["numberNp"])
        assert len(c["dateMap"]) == len(BUNDLED_CONSTANTS["dateMap"])
        assert c["dateMap"][0] == {
            "year": 1976,
            "days": BUNDLED_CONSTANTS["dateMap"][0]["days"],
        }

    def test_none_behaves_like_no_overrides(self):
        assert define_constants(None) == define_constants({})

    def test_never_shares_lists_with_the_bundled_data_or_the_input(self):
        c = define_constants()
        assert c["dateMap"] is not BUNDLED_CONSTANTS["dateMap"]
        assert c["dateMap"][0]["days"] is not BUNDLED_CONSTANTS["dateMap"][0]["days"]
        assert c["monthEn"] is not BUNDLED_CONSTANTS["monthEn"]

        mine = names(12, "X")
        d = define_constants({"monthEn": mine})
        mine[0] = "changed"
        assert d["monthEn"][0] == "X0"

    def test_falls_back_to_bundled_values_for_anything_not_overridden(self):
        c = define_constants({"monthEn": names(12, "X")})
        assert c["monthEn"][0] == "X0"
        assert c["weekEn"] == list(BUNDLED_CONSTANTS["weekEn"])
        assert len(c["dateMap"]) == len(BUNDLED_CONSTANTS["dateMap"])

    def test_explicit_none_values_are_ignored(self):
        c = define_constants({"monthEn": None})  # type: ignore[typeddict-item]
        assert c["monthEn"] == list(BUNDLED_CONSTANTS["monthEn"])

    def test_accepts_processed_bundled_entries_and_extra_years(self):
        c = define_constants({"dateMap": [*BUNDLED_CONSTANTS["dateMap"], EXTRA_YEAR]})
        assert len(c["dateMap"]) == len(BUNDLED_CONSTANTS["dateMap"]) + 1
        assert c["dateMap"][-1]["year"] == 2101
        # processed-only fields are stripped from the raw output
        assert sorted(c["dateMap"][0].keys()) == ["days", "year"]

    def test_accepts_tuples_and_integral_floats(self):
        c = define_constants(
            {
                "epoch": float(CUSTOM_EPOCH),  # type: ignore[typeddict-item]
                "monthEn": tuple(names(12, "T")),  # type: ignore[typeddict-item]
            }
        )
        assert c["epoch"] == CUSTOM_EPOCH
        assert isinstance(c["epoch"], int)
        assert c["monthEn"][0] == "T0"

    def test_rejects_unknown_keys_so_typos_do_not_pass_silently(self):
        with pytest.raises(ValueError, match='unknown key "monthEN"'):
            define_constants({"monthEN": []})  # type: ignore[typeddict-unknown-key]

    def test_validates_the_merged_result(self):
        with pytest.raises(ValueError, match="monthEn must be a list of exactly 12"):
            define_constants({"monthEn": ["only", "two"]})


# ----------------------------------------------------------------------------------------------
# validate_constants
# ----------------------------------------------------------------------------------------------
def raw_with(**override):
    base = {key: BUNDLED_CONSTANTS[key] for key in BUNDLED_CONSTANTS}
    base.update(override)
    return base


class TestValidateConstants:
    def test_accepts_the_bundled_constants(self):
        validate_constants(BUNDLED_CONSTANTS)

    def test_accepts_32_day_months_and_a_negative_offset(self):
        validate_constants(
            raw_with(dateMap=[{"year": 1, "days": [32] * 12}], utcOffsetMs=-3_600_000)
        )

    @pytest.mark.parametrize(
        "override, pattern",
        [
            ({"dateMap": []}, "dateMap must be a non-empty list"),
            ({"dateMap": "nope"}, "dateMap must be a non-empty list"),
            (
                {"dateMap": [{"year": "x", "days": [30] * 12}]},
                "year must be an integer",
            ),
            (
                {"dateMap": [{"year": True, "days": [30] * 12}]},
                "year must be an integer",
            ),
            ({"dateMap": [42]}, "year must be an integer"),
            ({"dateMap": [{"days": [30] * 12}]}, "year must be an integer"),
            (
                {"dateMap": [thirty(3000), thirty(3002)]},
                "expected 3001 at index 1 but got 3002",
            ),
            ({"dateMap": [thirty(3001), thirty(3000)]}, "consecutive"),
            (
                {"dateMap": [{"year": 3000, "days": [30, 30]}]},
                "exactly 12 month lengths",
            ),
            (
                {"dateMap": [{"year": 3000, "days": [30] * 13}]},
                "exactly 12 month lengths",
            ),
            ({"dateMap": [{"year": 3000, "days": "30"}]}, "exactly 12 month lengths"),
            ({"dateMap": [{"year": 3000}]}, "exactly 12 month lengths"),
            (
                {"dateMap": [{"year": 3000, "days": [0] + [30] * 11}]},
                "month 1 of year 3000",
            ),
            (
                {"dateMap": [{"year": 3000, "days": [30] * 11 + [33]}]},
                "month 12 of year 3000",
            ),
            ({"dateMap": [{"year": 3000, "days": [30.5] + [30] * 11}]}, "month 1"),
            ({"dateMap": [{"year": 3000, "days": ["30"] + [30] * 11}]}, "month 1"),
            ({"dateMap": [{"year": 3000, "days": [True] + [30] * 11}]}, "month 1"),
            ({"epoch": 1.5}, "epoch must be an integer"),
            ({"epoch": float("nan")}, "epoch must be an integer"),
            ({"epoch": "abc"}, "epoch must be an integer"),
            ({"epoch": True}, "epoch must be an integer"),
            ({"epoch": DEFAULT_EPOCH + 1}, "UTC midnight"),
            ({"utcOffsetMs": float("nan")}, "utcOffsetMs must be a finite number"),
            ({"utcOffsetMs": float("inf")}, "utcOffsetMs must be a finite number"),
            ({"utcOffsetMs": "5"}, "utcOffsetMs must be a finite number"),
            ({"utcOffsetMs": True}, "utcOffsetMs must be a finite number"),
            ({"weekEn": ["a"]}, "weekEn must be a list of exactly 7"),
            ({"weekShortEn": names(8, "x")}, "weekShortEn must be a list of exactly 7"),
            ({"weekNp": "abcdefg"}, "weekNp must be a list of exactly 7"),
            ({"weekShortNp": names(6, "x")}, "weekShortNp must be a list of exactly 7"),
            ({"monthEn": names(11, "x")}, "monthEn must be a list of exactly 12"),
            (
                {"monthShortEn": names(13, "x")},
                "monthShortEn must be a list of exactly 12",
            ),
            ({"monthNp": []}, "monthNp must be a list of exactly 12"),
            (
                {"monthShortNp": names(1, "x")},
                "monthShortNp must be a list of exactly 12",
            ),
            ({"numberNp": names(9, "x")}, "numberNp must be a list of exactly 10"),
            ({"monthEn": [1] + names(11, "x")}, "monthEn must only contain strings"),
        ],
    )
    def test_rejects_invalid_shapes_with_a_readable_message(self, override, pattern):
        with pytest.raises(ValueError, match=pattern):
            validate_constants(raw_with(**override))

    @pytest.mark.parametrize("key", list(BUNDLED_CONSTANTS.keys()))
    def test_reports_missing_keys_and_points_to_define_constants(self, key):
        partial = {k: v for k, v in BUNDLED_CONSTANTS.items() if k != key}
        with pytest.raises(ValueError, match=rf"missing '{key}'.*define_constants"):
            validate_constants(partial)

    def test_rejects_non_mappings(self):
        for bad in (None, [], "constants", 5):
            with pytest.raises(ValueError, match="constants must be a mapping"):
                validate_constants(bad)  # type: ignore[arg-type]

    def test_messages_carry_a_prefix(self):
        with pytest.raises(ValueError, match=r"^Invalid Nepali constants: "):
            validate_constants(raw_with(epoch=float("nan")))


# ----------------------------------------------------------------------------------------------
# process_constants / find_year_index
# ----------------------------------------------------------------------------------------------
class TestProcessConstants:
    def test_computes_cumulative_days(self):
        p = process_constants(CAL)
        assert [e["totalDays"] for e in p["dateMap"]] == [366, 360, 372]
        assert [e["daysTillNow"] for e in p["dateMap"]] == [366, 726, 1098]

    def test_returns_a_read_only_snapshot(self):
        p = process_constants(CAL)
        with pytest.raises(TypeError):
            p["epoch"] = 0  # type: ignore[index]
        with pytest.raises(TypeError):
            p["dateMap"][0]["year"] = 1  # type: ignore[index]
        with pytest.raises(TypeError):
            p["dateMap"][0]["days"][0] = 99  # type: ignore[index]
        with pytest.raises(TypeError):
            p["monthEn"][0] = "x"  # type: ignore[index]

    def test_does_not_alias_or_modify_the_input(self):
        raw = define_constants({"dateMap": [thirty(1)]})
        before = (list(raw["dateMap"][0]["days"]), list(raw["monthEn"]))
        p = process_constants(raw)
        raw["dateMap"][0]["days"][0] = 32
        raw["monthEn"][0] = "Hacked"
        assert p["dateMap"][0]["days"][0] == 30
        assert p["monthEn"][0] == before[1][0]

    def test_validates_before_processing(self):
        with pytest.raises(ValueError, match="epoch"):
            process_constants(raw_with(epoch=float("nan")))


class TestFindYearIndex:
    date_map = process_constants(CAL)["dateMap"]

    @pytest.mark.parametrize(
        "offset, expected",
        [(0, 0), (365, 0), (366, 1), (725, 1), (726, 2), (1097, 2)],
    )
    def test_boundaries(self, offset, expected):
        assert find_year_index(self.date_map, offset) == expected

    def test_agrees_with_a_linear_scan_over_every_day_of_the_bundled_calendar(self):
        bundled = BUNDLED_CONSTANTS["dateMap"]
        last = bundled[-1]["daysTillNow"]
        expected = 0
        for d in range(last):
            while d >= bundled[expected]["daysTillNow"]:
                expected += 1
            assert find_year_index(bundled, d) == expected

    def test_single_year(self):
        single = process_constants(define_constants({"dateMap": [thirty(5)]}))[
            "dateMap"
        ]
        assert find_year_index(single, 0) == 0
        assert find_year_index(single, 359) == 0


# ----------------------------------------------------------------------------------------------
# Resolution, caching, isolation
# ----------------------------------------------------------------------------------------------
class TestConstantsResolution:
    def test_bundled_class_returns_the_bundled_object(self):
        assert NepaliDate.get_constants() is BUNDLED_CONSTANTS
        assert NepaliDate(2080, 0, 1).get_constants() is BUNDLED_CONSTANTS
        assert ymd(NepaliDate("2080-01-01")) == "2080-01-01"

    def test_same_snapshot_for_the_class_and_every_instance(self):
        first = Cal.get_constants()
        assert Cal.get_constants() is first
        assert Cal(3000, 0, 1).get_constants() is first
        assert Cal(3001, 0, 1).get_constants() is first

    def test_classes_returning_the_same_raw_object_share_one_snapshot(self):
        other = make_class(CAL, "Other")
        assert other.get_constants() is Cal.get_constants()

    def test_calendars_are_isolated_from_each_other_and_from_the_default(self):
        small = make_class(
            define_constants({"dateMap": [{"year": 10, "days": [29] * 12}]}), "Small"
        )
        assert small.get_constants() is not Cal.get_constants()
        assert NepaliDate.get_constants() is BUNDLED_CONSTANTS
        assert small(10, 0, 1).days_in_month() == 29
        assert Cal(3000, 0, 1).days_in_month() == 30
        assert NepaliDate(2080, 0, 1).days_in_month() == 31

    def test_constants_are_snapshotted_on_first_use(self):
        raw = define_constants({"dateMap": [thirty(1)]})
        snap = make_class(raw, "Snap")
        before = snap.get_constants()
        raw["dateMap"][0]["days"][0] = 32
        raw["monthEn"][0] = "Hacked"

        assert snap.get_constants() is before
        assert snap(1, 0, 1).days_in_month() == 30
        assert snap(1, 0, 1).format("MMMM") == "Baisakh"

    def test_replacing_the_constants_object_is_picked_up(self):
        current = {"value": define_constants({"dateMap": [thirty(1)]})}

        class Swap(NepaliDate):
            @classmethod
            def constants(cls):
                return current["value"]

        d = Swap(1, 0, 1)
        assert d.days_in_month() == 30
        current["value"] = define_constants(
            {"dateMap": [{"year": 1, "days": [31] * 12}]}
        )
        assert d.days_in_month() == 31

    def test_a_fresh_object_on_every_call_still_works(self):
        class Fresh(NepaliDate):
            @classmethod
            def constants(cls):
                return define_constants({"dateMap": [thirty(7)]})

        d = Fresh(7, 2, 3)
        assert ymd(d) == "7-03-03"
        assert d.days_in_month() == 30

    def test_hook_can_read_class_attributes(self):
        class Configurable(NepaliDate):
            calendar = CAL

            @classmethod
            def constants(cls):
                return cls.calendar

        alt = define_constants({"dateMap": [thirty(50)]})

        class AltConfigurable(Configurable):
            calendar = alt

        assert Configurable(3000, 0, 1).year == 3000
        assert AltConfigurable(50, 0, 1).year == 50
        with pytest.raises(ValueError, match="out of range"):
            AltConfigurable(3000, 0, 1)
        assert Configurable(3000, 0, 1).year == 3000

    def test_subclass_of_a_subclass_can_override_again(self):
        other = define_constants({"dateMap": [thirty(77)]})

        class Child(Cal):
            @classmethod
            def constants(cls):
                return other

        assert Child(77, 0, 1).year == 77
        with pytest.raises(ValueError, match="out of range"):
            Child(3000, 0, 1)
        assert Cal(3000, 0, 1).year == 3000

    def test_subclass_without_override_keeps_the_parent_calendar(self):
        class Plain(Cal):
            pass

        assert Plain.get_constants() is Cal.get_constants()
        assert ymd(Plain(3002, 3, 4)) == "3002-04-04"

    def test_the_cache_stays_bounded_and_still_returns_correct_data(self):
        classes = [
            make_class(define_constants({"dateMap": [thirty(100 + i)]}), f"C{i}")
            for i in range(80)
        ]
        for i, cls in enumerate(classes):
            assert cls(100 + i, 0, 1).year == 100 + i
        # the oldest entries were evicted; they are simply recomputed
        assert classes[0](100, 0, 1).year == 100
        assert classes[0].get_constants()["dateMap"][0]["year"] == 100

    def test_classmethod_hooks_can_be_called_on_instances(self):
        assert Cal(3000, 0, 1).constants() is CAL


class TestInvalidConstantsInASubclass:
    class Broken(NepaliDate):
        @classmethod
        def constants(cls):
            return {**BUNDLED_CONSTANTS, "dateMap": [{"year": 3000, "days": [30, 30]}]}

    def test_fail_fast_with_a_readable_message(self):
        Broken = self.Broken
        for call in (
            lambda: Broken(3000, 0, 1),
            lambda: Broken("3000-01-01"),
            lambda: Broken(),
            lambda: Broken.get_constants(),
            lambda: Broken.get_month_name(0),
            # a broken calendar is reported, not silently treated as "date is invalid"
            lambda: Broken.is_valid(3000, 0, 1),
            lambda: Broken.get_calendar_days(3000, 0),
        ):
            with pytest.raises(ValueError, match="Invalid Nepali constants"):
                call()

    def test_do_not_poison_other_classes(self):
        with pytest.raises(ValueError):
            self.Broken(3000, 0, 1)
        assert ymd(NepaliDate(2080, 0, 1)) == "2080-01-01"
        assert ymd(Cal(3000, 0, 1)) == "3000-01-01"

    def test_a_partial_dict_gets_a_pointer_to_define_constants(self):
        class Partial(NepaliDate):
            @classmethod
            def constants(cls):
                return {"dateMap": [thirty(3000)]}

        with pytest.raises(ValueError, match="missing 'epoch'.*define_constants"):
            Partial(3000, 0, 1)


# ----------------------------------------------------------------------------------------------
# Construction and parsing
# ----------------------------------------------------------------------------------------------
class TestConstruction:
    def test_year_month_day(self):
        d = Cal(3001, 5, 20)
        assert (d.get_year(), d.get_month(), d.get_date()) == (3001, 5, 20)
        assert ymd(d) == "3001-06-20"

    @pytest.mark.parametrize(
        "text", ["3000-02-15", "3000/02/15", "3000.02.15", "3000-2-15"]
    )
    def test_parses_every_separator(self, text):
        d = Cal(text)
        assert (d.year, d.month, d.day) == (3000, 1, 15)

    def test_partial_strings_default_to_first_month_and_day(self):
        assert ymd(Cal("3001")) == "3001-01-01"
        assert ymd(Cal("3001-04")) == "3001-04-01"

    @pytest.mark.parametrize("text", ["2080-01-01", "2999-12-30", "3003-01-01"])
    def test_rejects_strings_outside_the_custom_range(self, text):
        with pytest.raises(ValueError, match="Nepal year out of range"):
            Cal(text)

    @pytest.mark.parametrize("year", [2080, 2999, 3003])
    def test_rejects_numeric_dates_outside_the_custom_range(self, year):
        with pytest.raises(ValueError, match="Nepal year out of range!"):
            Cal(year, 0, 1)

    def test_uses_the_custom_month_lengths_when_validating(self):
        with pytest.raises(ValueError, match="Invalid Nepali date"):
            Cal("3001-01-31")
        assert Cal("3002-01-31").get_date() == 31
        with pytest.raises(ValueError, match="Invalid Nepali month"):
            Cal("3000-13-01")
        with pytest.raises(ValueError, match="Invalid Nepali month"):
            Cal("3000-00-01")
        with pytest.raises(ValueError, match="Invalid Nepali date"):
            Cal("3000-01-00")
        with pytest.raises(ValueError, match="Invalid date"):
            Cal("garbage")

    def test_parse_updates_an_instance(self):
        d = Cal(3000, 0, 1)
        d.parse("3001/03/04")
        assert ymd(d) == "3001-03-04"
        with pytest.raises(ValueError, match="Nepal year out of range"):
            d.parse("2080-01-01")

    def test_set_rolls_months_over_and_handles_negative_months(self):
        d = Cal(3000, 0, 1)
        d.set(3000, 12, 1)
        assert ymd(d) == "3001-01-01"
        d.set(3001, -1, 1)
        assert ymd(d) == "3000-12-01"

    def test_setters_go_through_the_custom_calendar(self):
        d = Cal(3000, 1, 31)
        d.set_year(3002)
        assert ymd(d) == "3002-02-31"
        d.set_month(5)
        assert ymd(d) == "3002-06-31"
        d.set_date(1)
        assert ymd(d) == "3002-06-01"

    def test_the_epoch_day_is_the_first_custom_day(self):
        assert (
            ymd(Cal(datetime.fromtimestamp(DEFAULT_EPOCH / 1000, tz=timezone.utc)))
            == "3000-01-01"
        )

    def test_instants_outside_the_range_are_rejected(self):
        with pytest.raises(ValueError, match="out of the supported range"):
            Cal(DEFAULT_EPOCH - DAY_MS)
        with pytest.raises(ValueError, match="out of the supported range"):
            Cal(DEFAULT_EPOCH + 1098 * DAY_MS)
        assert ymd(Cal(DEFAULT_EPOCH + 1097 * DAY_MS)) == "3002-12-31"

    def test_an_integer_alone_is_a_unix_timestamp_in_milliseconds(self):
        assert ymd(Cal(DEFAULT_EPOCH + 5 * DAY_MS)) == "3000-01-06"

    def test_rejects_invalid_argument_types(self):
        with pytest.raises(ValueError, match="Invalid argument syntax"):
            Cal(3.5)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="Invalid argument syntax"):
            Cal([])  # type: ignore[arg-type]


# ----------------------------------------------------------------------------------------------
# Long years regression
# ----------------------------------------------------------------------------------------------
class TestLongYears:
    def test_round_trips_every_day_of_a_372_day_year_calendar(self):
        count = 0
        for y in range(3000, 3005):
            for m in range(12):
                for d in range(1, 32):
                    date = Long(y, m, d)
                    assert (date.year, date.month, date.day) == (y, m, d)
                    count += 1
        assert count == 5 * 372

    def test_round_trips_every_day_of_the_mixed_calendar_through_timestamps(self):
        for n in range(1098):
            ts = DEFAULT_EPOCH + n * DAY_MS
            a = Cal(ts)
            b = Cal(a.year, a.month, a.day)
            assert b.get_time() == ts

    def test_walks_forward_one_day_at_a_time_without_gaps_or_repeats(self):
        d = Cal(3000, 0, 1)
        seen = {str(d)}
        for _ in range(1, 1098):
            d = d.add_days(1)
            assert str(d) not in seen
            seen.add(str(d))
        assert ymd(d) == "3002-12-31"
        assert len(seen) == 1098

    def test_the_bundled_calendar_still_converts_correctly(self):
        assert ymd(NepaliDate(utc_dt(2023, 4, 14))) == "2080-01-01"
        assert ymd(NepaliDate(DEFAULT_EPOCH)) == "1976-01-01"
        assert ymd(NepaliDate(NepaliDate.maximum())) == "2100-12-31"


# ----------------------------------------------------------------------------------------------
# Class-level helpers
# ----------------------------------------------------------------------------------------------
class TestClassLevelHelpers:
    def test_get_month_name(self):
        assert Cal.get_month_name(0) == "Month1"
        assert Cal.get_month_name(11) == "Month12"
        assert Cal.get_month_name(0, True) == "M1"
        assert Cal.get_month_name(0, False, True) == "NpMonth1"
        assert Cal.get_month_name(0, True, True) == "NM1"
        assert NepaliDate.get_month_name(0) == "Baisakh"

    def test_get_day_name(self):
        assert Cal.get_day_name(0) == "Day0"
        assert Cal.get_day_name(6, True) == "D6"
        assert Cal.get_day_name(1, False, True) == "NpDay1"
        assert Cal.get_day_name(1, True, True) == "ND1"
        assert NepaliDate.get_day_name(0) == "Sunday"

    def test_name_lookups_still_validate_their_index(self):
        with pytest.raises(ValueError, match="Invalid month index"):
            Cal.get_month_name(12)
        with pytest.raises(ValueError, match="Invalid month index"):
            Cal.get_month_name(-1)
        with pytest.raises(ValueError, match="Invalid day index"):
            Cal.get_day_name(7)

    def test_is_valid(self):
        assert Cal.is_valid(3000, 0, 1)
        assert Cal.is_valid(3002, 5, 31)
        assert not Cal.is_valid(3001, 0, 31)
        assert not Cal.is_valid(3000, 0, 0)
        assert not Cal.is_valid(3000, 12, 1)
        assert not Cal.is_valid(3000, -1, 1)
        assert not Cal.is_valid(2999, 0, 1)
        assert not Cal.is_valid(3003, 0, 1)
        assert not NepaliDate.is_valid(3000, 0, 1)
        assert NepaliDate.is_valid(2080, 0, 31)

    def test_minimum_and_maximum_follow_the_custom_calendar(self):
        assert Cal.minimum() == datetime.fromtimestamp(
            DEFAULT_EPOCH / 1000, tz=timezone.utc
        )
        assert int(Cal.maximum().timestamp() * 1000) == DEFAULT_EPOCH + 1097 * DAY_MS
        assert Cal.maximum().strftime("%Y-%m-%d") == ad_of(1097)

    def test_minimum_and_maximum_follow_a_custom_epoch(self):
        assert int(Utc.minimum().timestamp() * 1000) == CUSTOM_EPOCH
        assert int(Utc.maximum().timestamp() * 1000) == CUSTOM_EPOCH + 719 * DAY_MS

    def test_detached_calls_stay_bound_to_the_class(self):
        is_valid = Cal.is_valid
        get_month_name = NepaliDate.get_month_name
        assert is_valid(3000, 0, 1)
        assert get_month_name(0) == "Baisakh"

    def test_get_calendar_days_builds_the_grid_from_the_custom_calendar(self):
        grid = Cal.get_calendar_days(3001, 0)
        # 3001-01-01 is 366 days after the epoch (a Sunday), so a Tuesday
        assert grid["prev_remaining_days"] == 2
        assert grid["prev_month"] == {"year": 3000, "month": 11, "days": [30, 31]}
        assert grid["current_month"]["year"] == 3001
        assert len(grid["current_month"]["days"]) == 30
        assert grid["remaining_days"] == 42 - 2 - 30
        assert grid["next_month"]["year"] == 3001
        assert grid["next_month"]["month"] == 1
        assert len(grid["next_month"]["days"]) == 10

    def test_get_calendar_days_at_the_edges_leaves_the_missing_neighbour_empty(self):
        first = Cal.get_calendar_days(3000, 0)
        assert first["prev_remaining_days"] == 0
        assert first["prev_month"] == {"year": 0, "month": 0, "days": []}
        last = Cal.get_calendar_days(3002, 11)
        assert last["next_month"] == {"year": 0, "month": 0, "days": []}

    @pytest.mark.parametrize(
        "year, month", [(2080, 0), (3003, 0), (3000, 12), (3000, -1)]
    )
    def test_get_calendar_days_rejects_months_the_calendar_does_not_have(
        self, year, month
    ):
        with pytest.raises(ValueError, match="Invalid year or month"):
            Cal.get_calendar_days(year, month)

    def test_get_calendar_days_is_unavailable_on_the_default_class_for_custom_years(
        self,
    ):
        with pytest.raises(ValueError, match="Invalid year or month"):
            NepaliDate.get_calendar_days(3000, 0)

    def test_quarters_return_subclass_instances_for_an_explicit_year(self):
        q1 = Cal.get_quarter(1, 3001)
        assert isinstance(q1["start"], Cal)
        assert ymd(q1["start"]) == "3001-01-01"
        assert ymd(q1["end"]) == "3001-03-30"

        everything = Cal.get_quarters(3002)
        assert list(everything.keys()) == ["Q1", "Q2", "Q3", "Q4"]
        assert ymd(everything["Q4"]["start"]) == "3002-10-01"
        assert ymd(everything["Q4"]["end"]) == "3002-12-31"
        assert isinstance(everything["Q4"]["end"], Cal)

    def test_fiscal_quarters_cross_into_the_next_custom_year(self):
        q1 = Cal.get_fiscal_quarter(1, 3000)
        assert ymd(q1["start"]) == "3000-04-01"
        assert ymd(q1["end"]) == "3000-06-31"

        q4 = Cal.get_fiscal_quarter(4, 3000)
        assert ymd(q4["start"]) == "3001-01-01"
        assert ymd(q4["end"]) == "3001-03-30"

        everything = Cal.get_fiscal_quarters(3000)
        assert ymd(everything["Q3"]["start"]) == "3000-10-01"
        assert isinstance(everything["Q3"]["start"], Cal)

    def test_quarters_that_leave_the_range_or_are_invalid_raise(self):
        with pytest.raises(ValueError, match="Nepal year out of range!"):
            Cal.get_fiscal_quarter(4, 3002)
        with pytest.raises(ValueError, match="Nepal year out of range!"):
            Cal.get_quarter(1, 2080)
        with pytest.raises(ValueError, match="(?i)quarter"):
            Cal.get_quarter(5, 3000)
        with pytest.raises(ValueError, match="(?i)quarter"):
            Cal.get_fiscal_quarter(0, 3000)

    def test_current_date_helpers_raise_clearly_when_today_is_outside_the_custom_range(
        self,
    ):
        with pytest.raises(ValueError, match="out of the supported range"):
            Cal.current_fiscal_year()
        with pytest.raises(ValueError, match="out of the supported range"):
            Cal.get_quarter(1)


# ----------------------------------------------------------------------------------------------
# Instance behaviour
# ----------------------------------------------------------------------------------------------
class TestInstanceBehaviour:
    def test_days_in_month_leap_year_and_validity(self):
        d = Cal(3000, 0, 1)
        assert d.days_in_month() == 30
        assert Cal(3000, 1, 1).days_in_month() == 31
        assert Cal(3001, 0, 1).days_in_month() == 30
        assert Cal(3002, 5, 1).days_in_month() == 31
        assert d.is_leap_year()
        assert not Cal(3001, 0, 1).is_leap_year()
        assert Cal(3002, 0, 1).is_leap_year()
        assert d.is_valid_instance()

    def test_is_valid_instance_reports_tampered_fields(self):
        d = Cal(3001, 0, 1)
        d.day = 31
        assert not d.is_valid_instance()
        d.day = 30
        assert d.is_valid_instance()
        d.month = 12
        assert not d.is_valid_instance()
        d.month = 0
        d.year = 3003
        assert not d.is_valid_instance()
        d.year = 2999
        assert not d.is_valid_instance()

    def test_get_day_follows_the_epoch_weekday(self):
        assert Cal(3000, 0, 1).get_day() == 0
        assert Cal(3000, 0, 2).get_day() == 1
        assert Cal(3000, 1, 5).get_day() == 6
        assert Cal(3001, 0, 1).get_day() == 2

    def test_get_weeks_in_month(self):
        assert Cal(3001, 0, 10).get_weeks_in_month() == 5
        assert Cal(3000, 0, 1).get_weeks_in_month() == 5

    def test_add_days_keeps_the_subclass_and_crosses_years(self):
        d = Cal(3000, 11, 31).add_days(1)
        assert isinstance(d, Cal)
        assert ymd(d) == "3001-01-01"
        assert ymd(Cal(3001, 0, 1).add_days(-1)) == "3000-12-31"
        with pytest.raises(ValueError, match="out of the supported range"):
            Cal(3002, 11, 31).add_days(1)
        with pytest.raises(ValueError, match="out of the supported range"):
            Cal(3000, 0, 1).add_days(-1)

    def test_add_months_clamps_to_the_target_month_length(self):
        nxt = Cal(3000, 11, 31).add_months(1)
        assert isinstance(nxt, Cal)
        assert ymd(nxt) == "3001-01-30"
        assert ymd(Cal(3000, 1, 31).add_months(1)) == "3000-03-30"
        assert ymd(Cal(3001, 5, 15).add_months(-6)) == "3000-12-15"
        assert ymd(Cal(3000, 0, 1).add_months(24)) == "3002-01-01"
        with pytest.raises(
            ValueError, match="Resulting date is out of supported range"
        ):
            Cal(3000, 0, 1).add_months(-1)
        with pytest.raises(
            ValueError, match="Resulting date is out of supported range"
        ):
            Cal(3002, 11, 1).add_months(1)

    def test_add_years_clamps_and_keeps_the_subclass(self):
        up = Cal(3000, 1, 31).add_years(1)
        assert isinstance(up, Cal)
        assert ymd(up) == "3001-02-30"
        assert ymd(Cal(3000, 1, 31).add_years(2)) == "3002-02-31"
        assert ymd(Cal(3002, 1, 31).add_years(-2)) == "3000-02-31"
        with pytest.raises(
            ValueError, match="Resulting date is out of supported range"
        ):
            Cal(3000, 0, 1).add_years(3)
        with pytest.raises(
            ValueError, match="Resulting date is out of supported range"
        ):
            Cal(3000, 0, 1).add_years(-1)

    def test_clone_keeps_the_subclass_and_the_date(self):
        original = Cal(3001, 4, 9)
        copy = original.clone()
        assert isinstance(copy, Cal)
        assert copy is not original
        assert ymd(copy) == "3001-05-09"
        assert copy.get_time() == original.get_time()

    def test_start_and_end_helpers_keep_the_subclass(self):
        d = Cal(3001, 4, 9)
        assert isinstance(d.start_of_month(), Cal)
        assert ymd(d.start_of_month()) == "3001-05-01"
        assert ymd(d.end_of_month()) == "3001-05-30"
        assert ymd(d.start_of_year()) == "3001-01-01"
        assert ymd(d.end_of_year()) == "3001-12-30"
        assert ymd(Cal(3002, 0, 1).end_of_year()) == "3002-12-31"
        assert isinstance(d.end_of_year(), Cal)

    def test_start_and_end_of_week_use_the_custom_weekday(self):
        tuesday = Cal(3001, 0, 1)
        assert ymd(tuesday.start_of_week()) == "3000-12-30"
        assert ymd(tuesday.end_of_week()) == "3001-01-05"
        assert ymd(tuesday.start_of_week(1)) == "3000-12-31"
        assert isinstance(tuesday.start_of_week(), Cal)

    def test_start_and_end_of_day_stay_on_the_same_custom_day(self):
        d = Cal(3001, 4, 9)
        start, end = d.start_of_day(), d.end_of_day()
        assert ymd(start) == "3001-05-09"
        assert ymd(end) == "3001-05-09"
        assert end.get_time() - start.get_time() == DAY_MS - 1
        assert start.get_hours() == 0
        assert end.get_hours() == 23

    def test_comparisons_and_differences(self):
        a, b = Cal(3000, 0, 1), Cal(3001, 2, 1)
        assert b.diff(a, "year") == 1
        assert b.diff(a, "month") == 14
        assert b.diff(a, "day") == 366 + 60
        assert a.is_before(b)
        assert b.is_after(a)
        assert a.is_equal(a.clone())
        assert a.is_same(Cal(3000, 5, 5), "year")
        assert not a.is_same(Cal(3000, 5, 5), "month")
        assert a < b and b > a
        assert a == a.clone()

    def test_str_and_get_english_date(self):
        d = Cal(3000, 0, 6)
        assert str(d) == "3000/1/6"
        assert d.get_english_date().strftime("%Y-%m-%d") == ad_of(5)


# ----------------------------------------------------------------------------------------------
# Formatting
# ----------------------------------------------------------------------------------------------
class TestFormatting:
    d = Cal(3000, 1, 5)  # Saturday, month index 1

    @pytest.mark.parametrize(
        "fmt, expected",
        [
            ("MMMM", "Month2"),
            ("MMM", "M2"),
            ("DDDD", "Day6"),
            ("DDD", "D6"),
            ("mmmm", "NpMonth2"),
            ("mmm", "NM2"),
            ("dddd", "NpDay6"),
            ("ddd", "ND6"),
            # 3000 -> d a a a, month 2 -> c, day 5 -> f
            ("yyyy", "daaa"),
            ("yy", "aa"),
            ("yyy", "aaa"),
            ("m", "c"),
            ("mm", "ac"),
            ("d", "f"),
            ("dd", "af"),
            ("yyyy-mm-dd", "daaa-ac-af"),
            # English digits are untouched by the Nepali digit table
            ("YYYY-MM-DD", "3000-02-05"),
            ("M-D", "2-5"),
        ],
    )
    def test_custom_labels_and_digits(self, fmt, expected):
        assert self.d.format(fmt) == expected

    def test_the_default_class_keeps_its_own_labels(self):
        assert NepaliDate(2080, 0, 1).format("MMMM DDDD") == "Baisakh Friday"
        assert NepaliDate(2080, 0, 1).format("mmmm dd") == "बैशाख ०१"

    def test_a_partial_override_only_changes_what_it_names(self):
        partial = make_class(
            define_constants({"monthEn": names(12, "Only")}), "Partial"
        )
        p = partial(2080, 0, 1)
        assert p.format("MMMM") == "Only0"
        assert p.format("DDDD") == "Friday"
        assert p.format("mmmm") == "बैशाख"


# ----------------------------------------------------------------------------------------------
# Extending the real calendar
# ----------------------------------------------------------------------------------------------
class TestExtendedCalendar:
    def test_supports_the_new_year_while_the_default_class_still_rejects_it(self):
        assert ymd(Extended(2101, 0, 1)) == "2101-01-01"
        with pytest.raises(ValueError, match="Nepal year out of range!"):
            NepaliDate(2101, 0, 1)
        assert Extended.is_valid(2101, 11, 31)
        assert not NepaliDate.is_valid(2101, 11, 31)

    @pytest.mark.parametrize(
        "ymd_tuple",
        [(1976, 0, 1), (2000, 5, 15), (2080, 0, 1), (2081, 6, 30), (2100, 11, 31)],
    )
    def test_agrees_with_the_default_class_on_shared_dates(self, ymd_tuple):
        base, ext = NepaliDate(*ymd_tuple), Extended(*ymd_tuple)
        assert ext.get_time() == base.get_time()
        assert ext.format("YYYY-MM-DD dddd") == base.format("YYYY-MM-DD dddd")

    def test_lifts_the_maximum_by_exactly_the_added_year(self):
        added = sum(EXTRA_YEAR["days"])
        delta = Extended.maximum().timestamp() - NepaliDate.maximum().timestamp()
        assert round(delta * 1000) == added * DAY_MS
        assert Extended.minimum() == NepaliDate.minimum()

    def test_converts_the_day_after_the_old_maximum_only_in_the_subclass(self):
        after = datetime.fromtimestamp(
            NepaliDate.maximum().timestamp() + 86400, tz=timezone.utc
        )
        with pytest.raises(ValueError, match="out of the supported range"):
            NepaliDate(after)
        assert ymd(Extended(after)) == "2101-01-01"

    def test_arithmetic_across_the_old_boundary(self):
        assert ymd(Extended(2100, 5, 10).add_years(1)) == "2101-06-10"
        assert ymd(Extended(2101, 0, 1).end_of_year()) == "2101-12-31"

    def test_a_corrected_month_length_only_affects_the_subclass(self):
        patched = [
            {
                "year": e["year"],
                "days": (
                    ([32] + list(e["days"][1:]))
                    if e["year"] == 2080
                    else list(e["days"])
                ),
            }
            for e in BUNDLED_CONSTANTS["dateMap"]
        ]
        fixed = make_class(define_constants({"dateMap": patched}), "Fixed")
        assert NepaliDate(2080, 0, 1).days_in_month() == 31
        assert fixed(2080, 0, 1).days_in_month() == 32
        assert fixed.is_valid(2080, 0, 32)
        assert not NepaliDate.is_valid(2080, 0, 32)
        assert (
            fixed(2080, 1, 1).get_time() == NepaliDate(2080, 1, 1).get_time() + DAY_MS
        )


# ----------------------------------------------------------------------------------------------
# Custom epoch and offset
# ----------------------------------------------------------------------------------------------
class TestEpochAndOffset:
    def test_a_custom_epoch_maps_to_the_first_day(self):
        assert ymd(Utc(CUSTOM_EPOCH)) == "1-01-01"
        assert Utc(1, 0, 1).get_time() == CUSTOM_EPOCH
        assert Utc(1, 1, 1).get_time() == CUSTOM_EPOCH + 30 * DAY_MS
        assert Utc(2, 11, 30).get_time() == CUSTOM_EPOCH + 719 * DAY_MS

    def test_time_of_day_getters_use_the_custom_offset(self):
        instant = utc_dt(2000, 1, 31, 13, 30, 15, 250)
        u = Utc(instant)
        assert (u.year, u.month, u.day) == (1, 1, 1)
        assert u.get_hours() == 13
        assert u.get_minutes() == 30
        assert u.get_seconds() == 15
        assert u.get_milliseconds() == 250

        p = Plus5(instant)
        assert p.get_hours() == 18
        assert p.get_minutes() == 30

    def test_the_offset_can_push_an_instant_onto_the_next_local_day(self):
        late = utc_dt(2000, 1, 1, 20, 0)
        assert Utc(late).day == 1
        assert Plus5(late).day == 2

    def test_start_and_end_of_day_respect_the_offset(self):
        p = Plus5(utc_dt(2000, 1, 1, 20, 0))
        assert p.start_of_day().get_hours() == 0
        assert p.end_of_day().get_hours() == 23
        assert p.start_of_day().day == 2

    def test_instants_outside_a_custom_epoch_range_are_rejected(self):
        with pytest.raises(ValueError, match="out of the supported range"):
            Utc(CUSTOM_EPOCH - 1)
        with pytest.raises(ValueError, match="out of the supported range"):
            Utc(CUSTOM_EPOCH + 720 * DAY_MS)

    def test_a_negative_offset(self):
        w = West(utc_dt(2000, 1, 2, 1, 0))
        assert w.day == 1
        assert w.get_hours() == 22


# ----------------------------------------------------------------------------------------------
# Copy constructor
# ----------------------------------------------------------------------------------------------
class TestCopyConstructor:
    def test_copy_within_the_same_calendar_keeps_the_fields(self):
        original = Cal(3001, 4, 9)
        copy = Cal(original)
        assert (copy.year, copy.month, copy.day) == (3001, 4, 9)
        assert copy.get_time() == original.get_time()

    def test_copy_between_the_default_class_and_a_subclass_sharing_its_calendar(self):
        class SameCalendar(NepaliDate):
            pass

        copy = SameCalendar(NepaliDate(2080, 5, 6))
        assert ymd(copy) == "2080-06-06"
        assert ymd(NepaliDate(copy)) == "2080-06-06"

    def test_copy_across_different_calendars_recomputes_from_the_instant(self):
        shifted = make_class(
            define_constants(
                {
                    "epoch": utc_ms(2023, 4, 14),
                    "dateMap": [
                        {
                            "year": 2080,
                            "days": [30, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
                        }
                    ],
                }
            ),
            "Shifted",
        )
        # bundled Baisakh 2080 has 31 days, so day 31 there is day 1 of month 2
        # in the shifted calendar
        converted = shifted(NepaliDate(2080, 0, 31))
        assert (converted.year, converted.month, converted.day) == (2080, 1, 1)
        assert converted.is_valid_instance()
        assert converted.get_time() == NepaliDate(2080, 0, 31).get_time()

    def test_copy_across_calendars_does_not_keep_foreign_fields(self):
        with pytest.raises(ValueError, match="out of the supported range"):
            Cal(NepaliDate(2080, 0, 1))
        # both calendars share the default epoch, so the same instant is
        # 1976-01-01 in the bundled one
        assert ymd(NepaliDate(Cal(3000, 0, 1))) == "1976-01-01"


# ----------------------------------------------------------------------------------------------
# ADtoBS / BStoAD with a custom class
# ----------------------------------------------------------------------------------------------
class TestConverters:
    def test_use_the_subclass_calendar(self):
        assert ADtoBS("1919-04-13", Cal) == "3000-01-01"
        assert BStoAD("3000-01-01", Cal) == "1919-04-13"
        assert BStoAD("3001-01-01", Cal) == ad_of(366)
        assert BStoAD("3002-12-31", Cal) == ad_of(1097)
        assert ADtoBS(ad_of(726), Cal) == "3002-01-01"

    def test_round_trip_a_sample_of_custom_days(self):
        for n in range(0, 1098, 17):
            assert BStoAD(ADtoBS(ad_of(n), Cal), Cal) == ad_of(n)

    def test_report_conversion_failures_outside_the_custom_range(self):
        with pytest.raises(ValueError, match="Fail to convert AD to BS"):
            ADtoBS("2023-04-14", Cal)
        with pytest.raises(ValueError, match="Fail"):
            BStoAD("2080-01-01", Cal)
        with pytest.raises(ValueError, match="Fail"):
            BStoAD("3001-01-31", Cal)

    def test_keep_validating_the_input_shape(self):
        with pytest.raises(ValueError, match="Invalid date format"):
            ADtoBS("1919/04/13", Cal)
        with pytest.raises(ValueError, match="Invalid date format"):
            BStoAD("3000-1-1", Cal)

    def test_default_behaviour_is_unchanged_when_no_class_is_passed(self):
        assert ADtoBS("2023-04-14") == "2080-01-01"
        assert BStoAD("2080-01-01") == "2023-04-14"
        with pytest.raises(ValueError, match="Fail"):
            BStoAD("3000-01-01")
