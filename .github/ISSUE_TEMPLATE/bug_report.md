**Title:** `[BUG] `

**Describe the bug**
A clear and concise description of the bug in `nepali_date_library`. For example, wrong date conversion, unexpected output, or error thrown.

**To Reproduce**
Steps to reproduce the behavior:

```python
from nepali_date import NepaliDate

nd = NepaliDate("2026-03-16")
result = nd.format("YYYY-MM-DD")
print(result)
```

1. Run the above code (or your code that uses the library)
2. Observe the output/error

**Expected behavior**

```text
Expected output: "2079-12-02"
```

**Actual behavior**

```text
Actual output: "2079-11-31"  # incorrect date
```

**Environment (please complete the following information):**

- Python Version: [e.g. 3.11]
- Operating System: [e.g. Ubuntu 22.04, macOS 13]
- `nepali_date_library` Version: [e.g. 1.2.0]

**Logs / Stack Trace**
Paste any error messages or logs that appear.

**Additional context**
Add any other context about the problem here, e.g., edge cases, specific input dates, or system locale.
