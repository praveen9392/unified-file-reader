# Unified File Reader

A clean, extensible Python library for reading multiple file formats with a unified API. Built following Clean Code and Clean Architecture principles.

## Features

- **Unified API**: Single `read_file()` function for all supported formats
- **Multiple Formats**: CSV, JSON, TXT, XLSX, PDF, DOCX
- **Clean Architecture**: Modular, testable, and maintainable codebase
- **Extensible**: Add new file readers without modifying core logic
- **Type-Safe**: Full type hints for better IDE support
- **Well-Tested**: Comprehensive test suite with high coverage
- **Production-Ready**: PyPI packaging, logging, and error handling

## Requirements

Developed and tested on **Python 3.12.8** (recommended). Other versions within **3.9–3.12** should also work.

- pip (latest version recommended)
- Virtual environment tool (`python -m venv`)

See `requirements.txt` for the exact dependency versions used with Python 3.12.8.

## Installation

### From PyPI

```bash
pip install unified-file-reader
```

### From source (development setup)

```bash
# Clone the repository
git clone https://github.com/praveen9392/unified-file-reader.git
cd unified-file-reader

# Create a virtual environment (recommended)
python -m venv .venv

# Activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (cmd)
.venv\Scripts\activate.bat
# macOS / Linux
source .venv/bin/activate

# Install runtime + dev dependencies
pip install -e ".[dev]"

# Alternatively, to match exact versions from this repo
pip install -r requirements.txt
```

## Quick Start

```python
from unified_file_reader import read_file

# Read any supported file format
data = read_file("data.csv")
data = read_file("config.json")
data = read_file("document.pdf")
data = read_file("spreadsheet.xlsx")
```

## Supported Formats

| Format | Extension | Return Type | Notes |
|--------|-----------|-------------|-------|
| CSV | `.csv` | `List[Dict]` | Returns list of dictionaries |
| JSON | `.json` | `Any` | Preserves JSON structure |
| TXT | `.txt` | `str` | Returns plain text content |
| Excel | `.xlsx` | `List[Dict]` | Returns list of dictionaries |
| PDF | `.pdf` | `str` | Extracts all text content |
| DOCX | `.docx` | `str` | Extracts all paragraph text |

## Architecture Overview

```
unified_file_reader/
├── api.py                 # Public API entry point
├── registry.py            # Reader registry (dependency inversion)
├── exceptions.py          # Custom exceptions
├── interfaces/
│   └── base_reader.py     # Abstract reader contract
├── readers/               # Concrete implementations
│   ├── csv_reader.py
│   ├── json_reader.py
│   ├── txt_reader.py
│   ├── excel_reader.py
│   ├── pdf_reader.py
│   └── docx_reader.py
├── utils/
│   └── file_utils.py      # Utility functions
└── config/
    └── supported_formats.py
```

### Design Principles

- **Single Responsibility Principle (SRP)**: Each reader handles one format
- **Open/Closed Principle (OCP)**: Add new readers without modifying existing code
- **Liskov Substitution Principle (LSP)**: All readers implement the same interface
- **Interface Segregation Principle (ISP)**: Minimal, focused interfaces
- **Dependency Inversion Principle (DIP)**: High-level modules depend on abstractions

## Usage Examples

### Reading CSV Files

```python
from unified_file_reader import read_file

data = read_file("employees.csv")
# Returns: [{"name": "John", "age": "30"}, {"name": "Jane", "age": "28"}]

for row in data:
    print(f"{row['name']}: {row['age']}")
```

### Reading JSON Files

```python
config = read_file("config.json")
# Returns: {"database": {"host": "localhost", "port": 5432}}

print(config["database"]["host"])
```

### Reading Text Files

```python
content = read_file("document.txt")
# Returns: "This is the file content..."

print(content)
```

### Reading Excel Files

```python
data = read_file("report.xlsx")
# Returns: [{"Quarter": "Q1", "Revenue": 100000}, ...]

for row in data:
    print(f"{row['Quarter']}: ${row['Revenue']}")
```

### Reading PDF Files

```python
text = read_file("document.pdf")
# Returns: "Page 1 content...\nPage 2 content..."

print(text)
```

### Reading DOCX Files

```python
text = read_file("report.docx")
# Returns: "Paragraph 1...\nParagraph 2..."

print(text)
```

## Error Handling

```python
from unified_file_reader import read_file
from unified_file_reader.exceptions import UnsupportedFormatError, ReaderError

try:
    data = read_file("file.xyz")
except UnsupportedFormatError as e:
    print(f"Format not supported: {e}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ReaderError as e:
    print(f"Reading error: {e}")
```

## Extending with New Readers

To add support for a new file format:

1. Create a new reader class in `unified_file_reader/readers/`:

```python
from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists

class YAMLReader(BaseReader):
    supported_extensions = [".yaml", ".yml"]

    def can_read(self, extension: str) -> bool:
        return extension in self.supported_extensions

    def read(self, path: str):
        ensure_file_exists(path)
        import yaml
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
```

2. Register it in `unified_file_reader/registry.py`:

```python
from unified_file_reader.readers.yaml_reader import YAMLReader

readers = [
    # ... existing readers ...
    YAMLReader(),
]
```

3. Add tests in `tests/test_yaml_reader.py`

4. Update `supported_formats.py` with metadata

That's it! No changes needed to the core API.

## Testing

Run the test suite:

```bash
pytest
```

With coverage:

```bash
pytest --cov=unified_file_reader
```

Run specific tests:

```bash
pytest tests/test_api.py -v
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Format code:

```bash
black unified_file_reader tests
isort unified_file_reader tests
```

Type checking:

```bash
mypy unified_file_reader
```

Linting:

```bash
flake8 unified_file_reader tests
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Changelog

### v0.1.3
- Upgraded `pypdf` to `7.1.1` and `pandas` to `3.1.1`
- Modernized core dependencies in `requirements.txt` to latest stable releases
- Updated test & QA tooling (`pytest` 9.2.0, `mypy` 2.4.1, `black` 26.10.1)
- 100% test pass rate maintained (93 passed, 0 skipped, 0 failed)

### v0.1.2
- Modernized dev dependencies (`reportlab` for complete PDF testing)
- Aligned static type hints with strict `mypy` compliance
- Harmonized Flake8 configuration (`max-line-length = 100`) with Black and isort
- Added GitHub Pull Request template and `CHANGELOG.md`
- 100% test pass rate (93 passed, 0 skipped, 0 failed)

### v0.1.1
- Updated PyPI package version and metadata
- Enhanced Python 3.12 compatibility

### v0.1.0 (Initial Release)
- Initial release with support for CSV, JSON, TXT, XLSX, PDF, DOCX
- Clean Architecture implementation
- Full test coverage
- PyPI packaging

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
