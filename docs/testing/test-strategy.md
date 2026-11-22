# Testing Strategy & Test Suite

The test suite ensures that every reader handles both standard files and nasty edge cases without crashing unexpectedly.

---

## 1. Test Suite Layout
All tests live in `tests/` and use **`pytest`**:

```
tests/
├── conftest.py             # Shared fixtures and dynamic file generators
├── test_api.py             # Tests for the main read_file() entry point
├── test_csv_reader.py      # CSV parser tests (encodings, delimiters, headers)
├── test_json_reader.py     # JSON parser tests (objects, arrays, invalid syntax)
├── test_txt_reader.py      # Plain text reader tests (large files, special chars)
├── test_excel_reader.py    # Excel reader tests (NaN handling, multiple columns)
├── test_pdf_reader.py      # PDF reader tests (multi-page text, invalid streams)
├── test_docx_reader.py     # DOCX reader tests (paragraphs, empty lines)
├── test_registry.py        # Registry lookup and custom reader registration
└── test_file_utils.py      # Path validation and extension parsing tests
```

---

## 2. Running the Tests

Run the full test suite:
```bash
pytest
```

Run with coverage summary:
```bash
pytest --cov=unified_file_reader
```

Generate an interactive HTML coverage report:
```bash
pytest --cov=unified_file_reader --cov-report=html
# View report in your browser: htmlcov/index.html
```

Run tests for a single format:
```bash
pytest tests/test_pdf_reader.py -v
```

---

## 3. How Test Fixtures Work (`conftest.py`)
Rather than committing static sample files into the Git repository (which can clutter git history and get corrupted), all sample files are generated **on the fly** in temporary directories:

- `temp_dir`: Uses Python's `tempfile.TemporaryDirectory` fixture to create an isolated workspace that cleans itself up automatically when the test finishes.
- Dynamic builders generate real, binary `.xlsx` (using openpyxl), `.docx` (using python-docx), and `.pdf` files (using reportlab) during the test run.
- Because `reportlab` is installed as part of `pip install -e ".[dev]"`, PDF tests run seamlessly in all environments without skips.

---

## 4. Key Test Scenarios
- **Valid Files**: Check that tabular data returns `List[Dict]`, JSON preserves structure, and documents return string text.
- **Missing Files**: Verify `FileNotFoundError` is raised with a descriptive path.
- **Directories as Paths**: Ensure passing a folder raises a clear error.
- **Unsupported Extensions**: Verify `UnsupportedFormatError` is raised when trying to read unknown formats.
- **Corrupted / Invalid Files**: Ensure broken JSON or corrupt Word docs raise a clean `ReaderError` instead of uncaught internal tracebacks.
- **Case Sensitivity**: Verify `.CSV`, `.XLSX`, `.Pdf` match identically to `.csv`, `.xlsx`, `.pdf`.
- **Encoding Fallback**: Test CSV and text files saved with non-UTF-8 encodings to verify automatic fallback to Latin-1.
- **Custom Readers**: Confirm that registering a user-defined reader integrates cleanly without side effects.
