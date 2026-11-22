# Troubleshooting Guide

Common issues you might run into when working on or using `unified-file-reader`, and how to solve them.

---

## 1. `ModuleNotFoundError: No module named 'docx'` (or 'pypdf', 'pandas')
- **Why it happens**: Dependencies haven't been installed inside your current Python environment, or your terminal hasn't activated `.venv`.
- **Solution**:
  Make sure your virtual environment is active (you should see `(.venv)` in your shell prompt), then run:
  ```bash
  pip install -e ".[dev]"
  ```

---

## 2. PDF Tests Are Skipped (`reportlab not installed`)
- **Why it happens**: Generating dummy PDF files on the fly during testing requires `reportlab`. If `reportlab` is missing, pytest skips the PDF generation tests.
- **Solution**:
  Install `reportlab` or reinstall dev extras:
  ```bash
  pip install reportlab
  # or
  pip install -e ".[dev]"
  ```

---

## 3. PyPI Upload Fails with `403 Forbidden`
- **Why it happens**:
  1. PyPI no longer allows username/password authentication for uploads; you must use an API token.
  2. The API token was generated for a specific project other than `unified-file-reader`.
- **Solution**:
  1. Go to your PyPI account settings at [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/).
  2. Under **Scope**, select **Entire account (all projects)** or select the project `unified-file-reader`.
  3. When running Twine, supply:
     - **Username**: `__token__`
     - **Password**: `<your-pypi-token>` (starts with `pypi-...`)

---

## 4. `UnicodeDecodeError` on Foreign / Legacy Text Files
- **Why it happens**: The built-in text and CSV readers automatically try `utf-8` and fall back to `latin-1`. If your file is encoded in an unusual encoding like `shift-jis` (Japanese) or `utf-16`, decoding will fail.
- **Solution**:
  You can either convert the file to UTF-8 beforehand, or register a custom reader with the specific encoding required:
  ```python
  from unified_file_reader.readers.csv_reader import CSVReader
  import csv

  class ShiftJISCSVReader(CSVReader):
      supported_extensions = [".shiftjis.csv"]
      def read(self, path: str):
          with open(path, newline="", encoding="shift_jis") as f:
              return list(csv.DictReader(f))
  ```

---

## 5. Line Length Warnings in Flake8 (`E501 line too long`)
- **Why it happens**: Flake8 defaults to 79 characters, while our project standard uses Black's 100-character line length.
- **Solution**:
  Ensure you run `flake8` from the project root where the `.flake8` configuration file resides.
