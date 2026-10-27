import time
from nepali_date_library import NepaliDate, BUNDLED_CONSTANTS
from nepali_date_library.helper.nepali_constants import NepaliConstants


def test_default_constants_performance():
    date = NepaliDate()
    n = 1_000_000

    start = time.perf_counter()
    for _ in range(n):
        date._NepaliDate__get_constants()
    elapsed = time.perf_counter() - start

    micro_per_op = (elapsed * 1_000_000) / n
    print(f"\n[Python Benchmark] Default getConstants(): {micro_per_op:.4f} µs/op")
    assert micro_per_op < 1.0


def test_custom_constants_performance():
    custom_constants: NepaliConstants = {
        **BUNDLED_CONSTANTS,
        "dateMap": [
            {"year": 2080, "days": [31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 29, 31]},
            {"year": 2081, "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31]},
        ],
    }

    class CustomNepaliDate(NepaliDate):
        def _get_constants(self) -> NepaliConstants:
            return custom_constants

    custom_date = CustomNepaliDate(2080, 0, 1)

    # First call (processing)
    t0 = time.perf_counter()
    first = custom_date._NepaliDate__get_constants()
    first_run_micro = (time.perf_counter() - t0) * 1_000_000

    assert first["dateMap"][0]["totalDays"] == 364
    assert first["dateMap"][0]["daysTillNow"] == 364
    assert first["dateMap"][1]["daysTillNow"] == 730

    # Subsequent cached calls
    n = 1_000_000
    start = time.perf_counter()
    for _ in range(n):
        custom_date._NepaliDate__get_constants()
    cached_micro = ((time.perf_counter() - start) * 1_000_000) / n

    print(
        f"[Python Benchmark] Custom first-run process: {first_run_micro:.2f} µs | Cached calls: {cached_micro:.4f} µs/op"
    )
    assert cached_micro < 1.0


if __name__ == "__main__":
    test_default_constants_performance()
    test_custom_constants_performance()
    print("Python speed tester passed successfully!")

