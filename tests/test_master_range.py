"""
Full-range verification (BS 1976 - 2100), mirroring NodeJS/test/master.test.ts
and PHP's tests/MasterRangeTest.php.

For every single supported day, checks that BS -> AD -> BS round-trips
losslessly and that reconstructing a NepaliDate from the converted AD date
yields the identical BS date.
"""

from datetime import datetime
from nepali_date_library import NepaliDate, nepali_date_map, BStoAD, ADtoBS


def test_full_bs_to_ad_and_back():
    for year_data in nepali_date_map:
        year = year_data["year"]
        days_list = year_data["days"]
        for month_index, days_in_month in enumerate(days_list):
            for day in range(1, days_in_month + 1):
                nd = NepaliDate(year, month_index, day)
                expected = nd.format("YYYY-MM-DD")

                ad_date_str = BStoAD(expected)

                nd2 = NepaliDate(datetime.strptime(ad_date_str, "%Y-%m-%d"))
                bs_date_str = ADtoBS(ad_date_str)

                assert nd2.format("YYYY-MM-DD") == expected, (
                    f"Round-trip via AD mismatch for {expected} (AD {ad_date_str})"
                )
                assert bs_date_str == expected, (
                    f"ADtoBS mismatch for {expected} (AD {ad_date_str})"
                )
