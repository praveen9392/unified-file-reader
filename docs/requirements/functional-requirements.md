# Functional Requirements

## 1. Path Handling and Pre-Checks
- **Path Checking**: Before parsing begins, the library verifies that the path actually exists. If the file is missing, it immediately raises a standard `FileNotFoundError`.
- **Directory Protection**: If someone passes a path pointing to a folder instead of a file, the library catches it and raises an error (`FileNotFoundError` or `ValueError`) rather than trying to read it.
- **Case-Insensitive Extensions**: Files named `report.CSV`, `notes.Docx`, or `document.PDF` are matched properly just like their lowercase equivalents (`.csv`, `.docx`, `.pdf`).
- **Unregistered Extensions**: If you pass a file format that has no registered reader (e.g. `archive.tar.gz`), the library raises `UnsupportedFormatError`.

---

## 2. Format Reader Specifications

### CSV Files (`.csv`)
- Parses row data using the Python standard library's `csv.DictReader`.
- Decodes using `UTF-8` by default. If the file contains non-UTF-8 characters, it catches `UnicodeDecodeError` and automatically retries with `latin-1`.
- Returns rows as `List[Dict[str, Any]]` where keys match header names.

### JSON Files (`.json`)
- Loads JSON data using standard `json.load`.
- Preserves maps as `dict` and lists as `list`.
- If the file is corrupted or contains syntax errors, wraps the parser failure into a clean `ReaderError`.

### Plain Text Files (`.txt`)
- Reads the full file content into a Python string.
- Uses `UTF-8` encoding with automatic fallback to `latin-1`.
- Returns content as `str`.

### Excel Spreadsheets (`.xlsx`)
- Loads sheets via `pandas.read_excel` with `openpyxl`.
- Cleans missing spreadsheet cells (`NaN`) into clean Python `None` values.
- Converts records into a list of row dictionaries (`List[Dict[str, Any]]`).

### PDF Documents (`.pdf`)
- Iterates across document pages using `pypdf.PdfReader`.
- Extracts readable text from each page, joining them with newline separators.
- Returns full extracted content as `str`.

### Word Documents (`.docx`)
- Reads paragraphs through `python-docx.Document`.
- Concatenates paragraph text separated by newlines.
- Returns document body as `str`.

---

## 3. Custom Reader Registration
- Projects can define their own reader by subclassing `BaseReader` and implementing:
  - `supported_extensions: List[str]`
  - `can_read(extension: str) -> bool`
  - `read(path: str) -> Any`
- Calling `register_reader(MyReader())` dynamically exposes the format to `read_file(path)` across the entire application runtime.
