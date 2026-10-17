# Contributing to NepaliDate (Python) 🇳🇵

Thank you for your interest in contributing to the **NepaliDate Python Library**! This library provides an accurate, native implementation of Bikram Sambat date calculations for Python developers worldwide.

---

## 🛠️ Development Setup

This project uses [**uv**](https://docs.astral.sh/uv/) for high-speed package management, virtual environments, and task execution.

### Prerequisites

- Python 3.9 through 3.14
- `uv` (recommended) or `pip`

### 1. Clone & Setup Environment

```bash
git clone https://github.com/SandipGhimire/Nepali-Date-Library-Python.git
cd Nepali-Date-Library-Python

# Create virtual environment and install development dependencies
uv sync --group dev
```

### 2. Running Tests & Quality Checks

We use `taskipy` to run quality checks and tests in one command:

```bash
# Run code formatting check (black), linting (flake8), and unit tests (pytest)
uv run task test
```

Or run pytest directly:

```bash
uv run pytest
```

### 3. Code Formatting & Type Checking

Ensure your code adheres to standard Python formatting conventions before submitting:

```bash
# Auto-format source code with black
uv run black src tests

# Run flake8 linter
uv run flake8 src tests

# Run static type checking with mypy
uv run mypy src
```

### 4. Building the Package

```bash
uv run task build
```
This produces source distribution (`.tar.gz`) and binary wheels (`.whl`) in `dist/`.

---

## 🧪 Testing Guidelines

- All calendar calculations, conversions between BS and AD, leap year rules, and fiscal year calculations must be verified with comprehensive unit tests.
- When fixing an issue or adding a feature, add corresponding tests under `tests/`.

---

## 📚 Documentation

Detailed documentation and live converters are hosted centrally:

- **Documentation**: [https://nepali-pkg.date/docs/python](https://nepali-pkg.date/docs/python)
- **Live Converter**: [https://nepali-pkg.date/converter](https://nepali-pkg.date/converter)

---

## 🚀 Submitting a Pull Request

1. Fork the repo and create a new feature branch (`git checkout -b feat/your-feature-name`).
2. Implement your changes with accompanying tests.
3. Verify that `uv run task test` passes with zero errors or warnings.
4. Commit using descriptive conventional commit messages (e.g. `feat: add Devanagari weekday tokens`).
5. Open a Pull Request on GitHub and describe your changes clearly.

---

## 📄 License

By contributing to `nepali-date-library`, you agree that your contributions will be licensed under the [MIT License](./LICENSE).  
Made with ❤️ by [Sandip Ghimire](https://github.com/SandipGhimire).

