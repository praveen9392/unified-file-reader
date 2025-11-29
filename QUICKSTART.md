# Quick Start Guide

## Installation

Developed and tested on **Python 3.12.8** (recommended). Other versions within **3.9–3.12** should also work.

```bash
# Clone or download the project
cd unified-file-reader

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (cmd)
.venv\Scripts\activate.bat
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"

# Alternatively, to match exact versions from this repo
pip install -r requirements.txt
```

## Basic Usage

### Read a File
```python
from unified_file_reader import read_file

# CSV
data = read_file("data.csv")
# Returns: [{"name": "John", "age": "30"}, ...]

# JSON
config = read_file("config.json")
# Returns: {"key": "value", ...}

# Text
text = read_file("document.txt")
# Returns: "File content..."

# Excel
data = read_file("report.xlsx")
# Returns: [{"col1": "val1", ...}, ...]

# PDF
text = read_file("manual.pdf")
# Returns: "Extracted text from PDF..."

# DOCX
text = read_file("letter.docx")
# Returns: "Extracted text from document..."
```

### Error Handling
```python
from unified_file_reader import read_file
from unified_file_reader.exceptions import UnsupportedFormatError

try:
    data = read_file("file.xyz")
except UnsupportedFormatError:
    print("Format not supported")
except FileNotFoundError:
    print("File not found")
```

## Common Tasks

### Process CSV Data
```python
from unified_file_reader import read_file

data = read_file("employees.csv")

# Filter
seniors = [e for e in data if int(e["age"]) > 30]

# Group
by_dept = {}
for emp in data:
    dept = emp["department"]
    if dept not in by_dept:
        by_dept[dept] = []
    by_dept[dept].append(emp)
```

### Read Multiple Files
```python
from unified_file_reader import read_file

files = ["data1.csv", "data2.json", "data3.txt"]

for file in files:
    try:
        data = read_file(file)
        print(f"✓ Read {file}")
    except Exception as e:
        print(f"✗ Error reading {file}: {e}")
```

### Check Supported Formats
```python
from unified_file_reader.registry import get_supported_extensions

formats = get_supported_extensions()
print(f"Supported: {', '.join(formats)}")
# Output: Supported: .csv, .docx, .json, .pdf, .txt, .xlsx
```

### Use Direct Reader
```python
from unified_file_reader.registry import get_reader_for_extension

reader = get_reader_for_extension(".csv")
data = reader.read("data.csv")
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=unified_file_reader

# Run specific test
pytest tests/test_api.py -v

# Show output
pytest -s
```

## Development

### Format Code
```bash
black unified_file_reader tests
isort unified_file_reader tests
```

### Check Code Quality
```bash
flake8 unified_file_reader tests
mypy unified_file_reader
```

### Run All Checks
```bash
pytest && black --check unified_file_reader tests && flake8 unified_file_reader tests && mypy unified_file_reader
```

## Adding a New Format

### 1. Create Reader
```python
# unified_file_reader/readers/yaml_reader.py
from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists
import yaml

class YAMLReader(BaseReader):
    supported_extensions = [".yaml", ".yml"]
    
    def can_read(self, extension: str) -> bool:
        return extension.lower() in self.supported_extensions
    
    def read(self, path: str):
        ensure_file_exists(path)
        with open(path, 'r') as f:
            return yaml.safe_load(f)
```

### 2. Register
```python
# unified_file_reader/registry.py
from unified_file_reader.readers.yaml_reader import YAMLReader

_READERS = [
    # ... existing readers ...
    YAMLReader(),
]
```

### 3. Test
```python
# tests/test_yaml_reader.py
def test_read_yaml():
    reader = YAMLReader()
    data = reader.read("config.yaml")
    assert isinstance(data, dict)
```

### 4. Use
```python
from unified_file_reader import read_file

config = read_file("config.yaml")
```

## Project Structure

```
unified-file-reader/
├── unified_file_reader/      # Main package
│   ├── api.py               # Public API
│   ├── registry.py          # Reader registry
│   ├── exceptions.py        # Custom exceptions
│   ├── interfaces/          # Abstract contracts
│   ├── readers/             # Concrete readers
│   ├── utils/               # Utilities
│   └── config/              # Configuration
├── tests/                   # Test suite
├── examples/                # Example scripts
├── README.md               # User guide
├── ARCHITECTURE.md         # Architecture docs
├── DEVELOPMENT.md          # Dev guide
└── pyproject.toml          # Package config
```

## Key Files

| File | Purpose |
|------|---------|
| `api.py` | Public API entry point |
| `registry.py` | Maps extensions to readers |
| `interfaces/base_reader.py` | Abstract reader interface |
| `readers/*.py` | Format-specific readers |
| `utils/file_utils.py` | Common utilities |
| `exceptions.py` | Custom exceptions |

## Supported Formats

| Format | Extension | Return Type |
|--------|-----------|-------------|
| CSV | `.csv` | `List[Dict]` |
| JSON | `.json` | `Any` |
| Text | `.txt` | `str` |
| Excel | `.xlsx` | `List[Dict]` |
| PDF | `.pdf` | `str` |
| DOCX | `.docx` | `str` |

## Documentation

- **README.md** - Full user guide
- **ARCHITECTURE.md** - System design
- **DEVELOPMENT.md** - Development guide
- **CONTRIBUTING.md** - How to contribute
- **examples/basic_usage.py** - Common examples
- **examples/advanced_usage.py** - Advanced patterns

## Troubleshooting

### Import Error
```bash
pip install -e .
```

### Test Failures
```bash
pytest -v -s
```

### Type Errors
```bash
mypy unified_file_reader
```

## Next Steps

1. ✅ Read the [README.md](README.md)
2. ✅ Check [examples/basic_usage.py](examples/basic_usage.py)
3. ✅ Review [ARCHITECTURE.md](ARCHITECTURE.md)
4. ✅ Run the tests: `pytest`
5. ✅ Start using: `from unified_file_reader import read_file`

## Support

- Check [README.md](README.md) for detailed documentation
- Review [examples/](examples/) for usage patterns
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for design details
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development info

## License

MIT License - Free for commercial and personal use
