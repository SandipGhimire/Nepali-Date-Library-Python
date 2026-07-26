from nepali_date_library import (
    nepali_date_map,
    number_np,
    week_en,
    week_np,
    week_short_en,
    week_short_np,
    month_en,
    month_np,
    month_short_en,
    month_short_np,
)


def test_week_arrays_have_7_entries_starting_with_sunday():
    for arr in (week_en, week_np, week_short_en, week_short_np):
        assert len(arr) == 7
    assert week_en[0] == "Sunday"
    assert week_short_en[0] == "Sun"


def test_month_arrays_have_12_entries_starting_with_baisakh():
    for arr in (month_en, month_np, month_short_en, month_short_np):
        assert len(arr) == 12
    assert month_en[0] == "Baisakh"
    assert month_short_en[0] == "Bai"


def test_number_np_maps_digits_0_9_to_devanagari_numerals():
    assert len(number_np) == 10
    assert number_np[0] == "०"
    assert number_np[9] == "९"


def test_nepali_date_map_starts_at_1976_and_each_year_has_12_months():
    assert nepali_date_map[0]["year"] == 1976
    for year_data in nepali_date_map:
        assert len(year_data["days"]) == 12
