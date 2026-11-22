# Requirements Overview

## Motivation
In most Python projects, handling data from different file types means pulling in several distinct libraries:
- `csv` or `pandas` for CSVs
- `json` for config and payloads
- `pandas` and `openpyxl` for Excel spreadsheets
- `pypdf` for PDF text extraction
- `python-docx` for Word documents

Each library comes with its own quirks, different method calls, varied parameter conventions, and completely different output shapes. 

**Unified File Reader** exists to cut down on that boilerplate. You point `read_file(path)` at a file, and it delegates to the right reader and gives you back clean, predictable Python data structures.

---

## Core Principles
1. **One Import**: Read any supported file with just `from unified_file_reader import read_file`.
2. **Automatic Format Detection**: The library checks the file extension (case-insensitively) and picks the right parser.
3. **Consistent Return Shapes**: Tabular formats return rows as lists of dictionaries (`List[Dict]`), structured payloads return native Python dictionaries or lists, and documents return cleaned plain text (`str`).
4. **Pluggable Architecture**: If your project needs to read a format that isn't built in (like YAML, Parquet, or XML), you can write a short reader class and register it without touching the core library code.

---

## Supported Formats

| Extension | Format | Parser Engine | Output Type | Typical Use |
| :--- | :--- | :--- | :--- | :--- |
| `.csv` | Comma-Separated Values | Standard library `csv.DictReader` | `List[Dict[str, Any]]` | Tabular row data |
| `.json` | JSON Documents | Standard library `json.load` | `Any` (dict / list) | Configuration & APIs |
| `.txt` | Plain Text | Native file I/O | `str` | Logs, notes, raw text |
| `.xlsx` | Microsoft Excel | `pandas` + `openpyxl` | `List[Dict[str, Any]]` | Spreadsheets & tables |
| `.pdf` | PDF Documents | `pypdf` | `str` | Text extracted from pages |
| `.docx` | Word Documents | `python-docx` | `str` | Paragraph text |
