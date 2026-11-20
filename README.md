# NepaliDate Library (Python) 🇳🇵

[![PyPI version](https://img.shields.io/pypi/v/nepali-date-library.svg?style=flat-square&color=E1804B)](https://pypi.org/project/nepali-date-library/)
[![Python versions](https://img.shields.io/pypi/pyversions/nepali-date-library.svg?style=flat-square&color=3776AB&logo=python&logoColor=white)](https://pypi.org/project/nepali-date-library/)
[![Documentation](https://img.shields.io/badge/Docs-nepali--pkg.date-E1804B?style=flat-square&logo=google-chrome&logoColor=white)](https://nepali-pkg.date/docs/python)
[![Date Converter](https://img.shields.io/badge/Converter-BS%20%E2%86%94%20AD-24292E?style=flat-square)](https://nepali-pkg.date/converter)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](./LICENSE)

A robust, zero-dependency Python library and **Nepali Date Converter** for working with **Nepali (Bikram Sambat / BS)** dates between **1976/01/01 and 2100/12/31 BS**.

---

### 📖 Full Documentation & Live Tools

All guides, complete API references, Devanagari format tokens, fiscal year helpers, and interactive playground are hosted on our official documentation portal:

👉 **[https://nepali-pkg.date/docs/python](https://nepali-pkg.date/docs/python)**  
🔄 **[Try the Live Date Converter](https://nepali-pkg.date/converter)**

---

## 📦 Installation

```bash
pip install nepali-date-library
```

> **Beta:** the pluggable-calendar-data release is a pre-release (`1.1.0b1`).
>
> ```bash
> pip install --pre nepali-date-library
> # or pin it
> pip install nepali-date-library==1.1.0b1
> ```

---

## 🚀 Quick Example

```python
from nepali_date_library import NepaliDate

today = NepaliDate()
print(today.format("YYYY-MM-DD"))  # "2081-07-01"
```

> **Note**: For complete API methods, standalone conversion (`ad_to_bs` / `bs_to_ad`), date arithmetic, and fiscal year calculations, visit [**https://nepali-pkg.date/docs/python**](https://nepali-pkg.date/docs/python).

---

## 🛠️ Custom Calendar Data

The calendar tables are replaceable, so you can add new years, fix a month length or change labels without waiting for a release. Subclass `NepaliDate`, override the `constants()` classmethod and return a dict built with `define_constants()`:

```python
from nepali_date_library import ADtoBS, BUNDLED_CONSTANTS, NepaliDate, define_constants

MY_CALENDAR = define_constants({
    # anything you leave out falls back to the bundled data
    "dateMap": [
        *BUNDLED_CONSTANTS["dateMap"],
        {"year": 2101, "days": [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31]},
    ],
})


class MyNepaliDate(NepaliDate):
    @classmethod
    def constants(cls):
        return MY_CALENDAR  # return the same object every time


MyNepaliDate(2101, 0, 1).format("YYYY-MM-DD")  # "2101-01-01"
MyNepaliDate.is_valid(2101, 0, 1)  # True (class helpers follow the subclass too)
ADtoBS("2044-04-13", MyNepaliDate)  # converters accept your class
```

Good to know:

- Settable keys: `dateMap`, `epoch`, `utcOffsetMs`, `weekEn`, `weekShortEn`, `weekNp`, `weekShortNp`, `monthEn`, `monthShortEn`, `monthNp`, `monthShortNp`, `numberNp`. Unknown keys raise `ValueError`.
- Constants are validated once (consecutive years, 12 months of 1-32 days, name tables of the right size, ...) and snapshotted on first use. Later edits to your dict are ignored; to change the calendar, return a different object.
- Time-dependent helpers such as `current_fiscal_year()` use today's date, so they raise if today is outside your calendar. Pass an explicit year in that case.

## 🤝 Contributing

Contributions are welcome! Please read our [**Contributing Guide**](./CONTRIBUTING.md) or visit our [**Online Contribution Guide**](https://nepali-pkg.date/docs/contribution).

---

## 📄 License

MIT © [Sandip Ghimire](https://github.com/SandipGhimire)  
Made with ❤️ by [Sandip Ghimire](https://github.com/SandipGhimire).
