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

---

## 🚀 Quick Example

```python
from nepali_date_library import NepaliDate

today = NepaliDate()
print(today.format("YYYY-MM-DD"))  # "2081-07-01"
```

> **Note**: For complete API methods, standalone conversion (`ad_to_bs` / `bs_to_ad`), date arithmetic, and fiscal year calculations, visit [**https://nepali-pkg.date/docs/python**](https://nepali-pkg.date/docs/python).

---

## 🤝 Contributing

Contributions are welcome! Please read our [**Contributing Guide**](./CONTRIBUTING.md) or visit our [**Online Contribution Guide**](https://nepali-pkg.date/docs/contribution).

---

## 📄 License

MIT © [Sandip Ghimire](https://github.com/SandipGhimire)  
Made with ❤️ by [Sandip Ghimire](https://github.com/SandipGhimire).
