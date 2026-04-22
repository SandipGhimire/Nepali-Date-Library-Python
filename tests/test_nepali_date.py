from datetime import datetime
from nepali_date_library import NepaliDate, nepali_date_map, BStoAD, ADtoBS


def test_full_bs_to_ad_and_back():
    for year_data in nepali_date_map:
        year = year_data["year"]
        days_list = year_data["days"]
        for month_index, days_in_month in enumerate(days_list):
            for day in range(1, days_in_month + 1):
                nd = NepaliDate(year, month_index, day)
                ad_date_str = BStoAD(nd.format("YYYY-MM-DD"))

                nd2 = NepaliDate(datetime.strptime(ad_date_str, "%Y-%m-%d"))
                bs_date_str = ADtoBS(ad_date_str)

                assert nd.format("YYYY-MM-DD") == nd2.format("YYYY-MM-DD")
                assert nd.format("YYYY-MM-DD") == bs_date_str
