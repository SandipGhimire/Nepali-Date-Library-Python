from typing import List
from .nepali_constants import (
    NepaliConstants,
    NepaliDateMapEntry,
    ProcessedDateMapEntry,
    ProcessedNepaliConstants,
)


def process_date_map(date_map: List[NepaliDateMapEntry]) -> List[ProcessedDateMapEntry]:
    total_days_accumulator = 0
    processed: List[ProcessedDateMapEntry] = []

    for entry in date_map:
        total_days = sum(entry["days"])
        total_days_accumulator += total_days
        processed.append(
            {
                "year": entry["year"],
                "days": entry["days"],
                "totalDays": total_days,
                "daysTillNow": total_days_accumulator,
            }
        )

    return processed


def process_constants(constants: NepaliConstants) -> ProcessedNepaliConstants:
    processed_map = process_date_map(constants.get("dateMap", []))
    res: ProcessedNepaliConstants = dict(constants)  # type: ignore
    res["dateMap"] = processed_map
    return res

