import pytest

from nepali_date_library import ADtoBS, BStoAD


def test_ad_to_bs_known_date():
    assert ADtoBS("2023-04-14") == "2080-01-01"


def test_bs_to_ad_known_date():
    assert BStoAD("2080-01-01") == "2023-04-14"


def test_round_trip():
    ad = "2023-04-28"
    bs = ADtoBS(ad)
    assert BStoAD(bs) == ad


def test_ad_to_bs_rejects_malformed_input():
    with pytest.raises(ValueError, match="Invalid date format. Expected format: YYYY-MM-DD"):
        ADtoBS("2023/04/14")


def test_bs_to_ad_rejects_malformed_input():
    with pytest.raises(ValueError, match="Invalid date format. Expected format: YYYY-MM-DD"):
        BStoAD("2080/01/01")


def test_ad_to_bs_rejects_out_of_range_date():
    with pytest.raises(ValueError):
        ADtoBS("1800-01-01")


def test_bs_to_ad_rejects_out_of_range_year():
    with pytest.raises(ValueError):
        BStoAD("1800-01-01")
