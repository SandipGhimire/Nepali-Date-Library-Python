from typing import TypedDict, List


class NepaliDateMapEntry(TypedDict):
    year: int
    days: List[int]


class ProcessedDateMapEntry(TypedDict):
    year: int
    days: List[int]
    totalDays: int
    daysTillNow: int


class NepaliConstants(TypedDict, total=False):
    dateMap: List[NepaliDateMapEntry]
    epoch: int
    utcOffsetMs: int
    weekEn: List[str]
    weekShortEn: List[str]
    weekNp: List[str]
    weekShortNp: List[str]
    monthEn: List[str]
    monthShortEn: List[str]
    monthNp: List[str]
    monthShortNp: List[str]
    numberNp: List[str]


class ProcessedNepaliConstants(TypedDict, total=False):
    dateMap: List[ProcessedDateMapEntry]
    epoch: int
    utcOffsetMs: int
    weekEn: List[str]
    weekShortEn: List[str]
    weekNp: List[str]
    weekShortNp: List[str]
    monthEn: List[str]
    monthShortEn: List[str]
    monthNp: List[str]
    monthShortNp: List[str]
    numberNp: List[str]
