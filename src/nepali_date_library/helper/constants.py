from datetime import datetime, timezone
from typing import TypedDict, List as TList


class NepaliDateEntry(TypedDict):
    year: int
    days: TList[int]
    totalDays: int
    daysTillNow: int


nepali_date_map: TList[NepaliDateEntry] = [
    {
        "year": 1976,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1977,
        "days": [30, 32, 31, 32, 31, 31, 29, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1978,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1979,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1980,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1981,
        "days": [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1982,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1983,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1984,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1985,
        "days": [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1986,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1987,
        "days": [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1988,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1989,
        "days": [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1990,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1991,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1992,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1993,
        "days": [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1994,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1995,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1996,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1997,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1998,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 1999,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2000,
        "days": [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2001,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2002,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2003,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2004,
        "days": [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2005,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2006,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2007,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2008,
        "days": [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2009,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2010,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2011,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2012,
        "days": [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2013,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2014,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2015,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2016,
        "days": [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2017,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2018,
        "days": [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2019,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2020,
        "days": [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2021,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2022,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2023,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2024,
        "days": [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2025,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2026,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2027,
        "days": [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2028,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2029,
        "days": [31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2030,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2031,
        "days": [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2032,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2033,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2034,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2035,
        "days": [30, 32, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2036,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2037,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2038,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2039,
        "days": [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2040,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2041,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2042,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2043,
        "days": [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2044,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2045,
        "days": [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2046,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2047,
        "days": [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2048,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2049,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2050,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2051,
        "days": [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2052,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2053,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2054,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2055,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2056,
        "days": [31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2057,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2058,
        "days": [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2059,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2060,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2061,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2062,
        "days": [30, 32, 31, 32, 31, 31, 29, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2063,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2064,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2065,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2066,
        "days": [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2067,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2068,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2069,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2070,
        "days": [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2071,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2072,
        "days": [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2073,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2074,
        "days": [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2075,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2076,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2077,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2078,
        "days": [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2079,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2080,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2081,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2082,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2083,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2084,
        "days": [31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2085,
        "days": [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2086,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2087,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2088,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2089,
        "days": [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2090,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2091,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2092,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2093,
        "days": [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2094,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2095,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2096,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2097,
        "days": [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2098,
        "days": [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2099,
        "days": [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        "totalDays": 0,
        "daysTillNow": 0,
    },
    {
        "year": 2100,
        "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        "totalDays": 0,
        "daysTillNow": 0,
    },
]

total_days = 0
for entry in nepali_date_map:
    entry["totalDays"] = sum(entry["days"])
    total_days += entry["totalDays"]
    entry["daysTillNow"] = total_days

# -----------------------------------------------------------------------------------
# Epoch Reference
# -----------------------------------------------------------------------------------
# Define the starting reference date for the Nepali calendar system (Bikram Sambat).
# The epoch is set to April 13, 1919 in UTC.
epoch_date = datetime(1919, 4, 13, tzinfo=timezone.utc)
EPOCH = int(epoch_date.timestamp() * 1000)

# -----------------------------------------------------------------------------------
# Weekdays
# -----------------------------------------------------------------------------------
# Full English names of the week.
week_en = ["Sunday", "Monday", "Tuesday",
           "Wednesday", "Thursday", "Friday", "Saturday"]

# Short English names of the week.
week_short_en = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

# Full Nepali names of the week.
week_np = ["आइतबार", "सोमबार", "मंगलबार",
           "बुधबार", "बिहिबार", "शुक्रबार", "शनिबार"]

# Short Nepali names of the week.
week_short_np = ["आइत", "सोम", "मंगल", "बुध", "बिहि", "शुक्र", "शनि"]

# -----------------------------------------------------------------------------------
# Months
# -----------------------------------------------------------------------------------
# Full names of Nepali months in English transliteration.
month_en = [
    "Baisakh",
    "Jestha",
    "Asar",
    "Shrawan",
    "Bhadra",
    "Aswin",
    "Kartik",
    "Mangsir",
    "Poush",
    "Magh",
    "Falgun",
    "Chaitra",
]

# Short names (abbreviations) of Nepali months in English transliteration.
month_short_en = [
    "Bai",
    "Jes",
    "Asa",
    "Shr",
    "Bhd",
    "Asw",
    "Kar",
    "Man",
    "Pou",
    "Mag",
    "Fal",
    "Cha",
]

# Full Nepali month names in Devanagari script.
month_np = [
    "बैशाख",
    "जेठ",
    "असार",
    "श्रावण",
    "भाद्र",
    "आश्विन",
    "कार्तिक",
    "मंसिर",
    "पौष",
    "माघ",
    "फाल्गुण",
    "चैत्र",
]

# Short Nepali month names (abbreviations) in Devanagari script.
month_short_np = [
    "बै",
    "जे",
    "अ",
    "श्रा",
    "भा",
    "आ",
    "का",
    "मं",
    "पौ",
    "मा",
    "फा",
    "चै",
]

# -----------------------------------------------------------------------------------
# Numbers
# -----------------------------------------------------------------------------------
# Nepali digits in Devanagari script.
number_np = ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"]
