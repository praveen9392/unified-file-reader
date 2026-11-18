# Development Guide

## Quick Start

### 1. Clone and Setup

Developed and tested on **Python 3.12.8** (recommended). Other versions within **3.9–3.12** should also work.

```bash
git clone https://github.com/praveen9392/unified-file-reader.git
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

# Install with dev dependencies
pip install -e ".[dev]"

# Or match exact versions from this repo
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
pytest
pytest --cov=unified_file_reader
black --check unified_file_reader tests
flake8 unified_file_reader tests
mypy unified_file_reader
isort --check unified_file_reader tests
```

## Development Commands

### Run Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=unified_file_reader --cov-report=html

# Specific test file
pytest tests/test_api.py

# Specific test
pytest tests/test_api.py::TestReadFileAPI::test_read_csv_file

# Verbose
pytest -v

# Show output
pytest -s
```

### Code Quality

#### Format Code
```bash
black unified_file_reader tests
isort unified_file_reader tests
```

#### Check Formatting
```bash
black --check unified_file_reader tests
isort --check-only unified_file_reader tests
```

#### Lint
```bash
flake8 unified_file_reader tests
```

#### Type Check
```bash
mypy unified_file_reader
```

#### All Checks
```bash
black unified_file_reader tests && \
isort unified_file_reader tests && \
flake8 unified_file_reader tests && \
mypy unified_file_reader && \
pytest
```

## Project Structure

```
unified-file-reader/
├── unified_file_reader/          # Main package
│   ├── __init__.py               # Package initialization
│   ├── api.py                    # Public API
│   ├── registry.py               # Reader registry
│   ├── exceptions.py             # Custom exceptions
│   ├── interfaces/               # Abstract contracts
│   │   ├── __init__.py
│   │   └── base_reader.py        # BaseReader interface
│   ├── readers/                  # Concrete readers
│   │   ├── __init__.py
│   │   ├── csv_reader.py
│   │   ├── json_reader.py
│   │   ├── txt_reader.py
│   │   ├── excel_reader.py
│   │   ├── pdf_reader.py
│   │   └── docx_reader.py
│   ├── utils/                    # Utilities
│   │   ├── __init__.py
│   │   └── file_utils.py
│   └── config/                   # Configuration
│       ├── __init__.py
│       └── supported_formats.py
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_api.py
│   ├── test_csv_reader.py
│   ├── test_json_reader.py
│   ├── test_txt_reader.py
│   ├── test_excel_reader.py
│   ├── test_pdf_reader.py
│   ├── test_docx_reader.py
│   ├── test_registry.py
│   └── test_file_utils.py
├── examples/                     # Example scripts
│   ├── __init__.py
│   ├── basic_usage.py
│   └── advanced_usage.py
├── pyproject.toml               # Project configuration
├── setup.py                     # Setup script
├── pytest.ini                   # Pytest configuration
├── requirements.txt             # Dependencies
├── README.md                    # User documentation
├── ARCHITECTURE.md              # Architecture documentation
├── CONTRIBUTING.md              # Contribution guidelines
├── DEVELOPMENT.md               # This file
└── LICENSE                      # MIT License
```

## Adding a New Reader

### 1. Create Reader File
Create `unified_file_reader/readers/xyz_reader.py`:

```python
from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists

class XYZReader(BaseReader):
    supported_extensions = [".xyz"]
    
    def can_read(self, extension: str) -> bool:
        return extension.lower() in self.supported_extensions
    
    def read(self, path: str):
        ensure_file_exists(path)
        # Implementation
```

### 2. Register Reader
Update `unified_file_reader/registry.py`:

```python
from unified_file_reader.readers.xyz_reader import XYZReader

_READERS = [
    # ... existing readers ...
    XYZReader(),
]
```

### 3. Add Tests
Create `tests/test_xyz_reader.py` with comprehensive tests.

### 4. Update Config
Update `unified_file_reader/config/supported_formats.py`:

```python
SUPPORTED_FORMATS = {
    # ... existing formats ...
    ".xyz": {
        "name": "XYZ Format",
        "description": "Description",
        "return_type": "Type",
        "reader_class": "XYZReader",
    },
}
```

### 5. Run Tests
```bash
pytest tests/test_xyz_reader.py -v
pytest --cov=unified_file_reader
```

## Testing Guidelines

### Unit Tests
- Test one thing per test
- Use descriptive names
- Use fixtures for setup
- Test error cases

### Integration Tests
- Test real file reading
- Test error handling
- Test edge cases

### Test Coverage
- Aim for >90% coverage
- All public APIs tested
- All error paths tested

### Running Tests
```bash
# All tests
pytest

# Coverage report
pytest --cov=unified_file_reader --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Code Style

### Python Style
- Follow PEP 8
- Use Black for formatting
- Use isort for imports
- Use type hints

### Naming
- Classes: PascalCase
- Functions: snake_case
- Constants: UPPER_SNAKE_CASE
- Private: _leading_underscore

### Imports
```python
# Standard library
import json
import os
from typing import Any, Dict, List

# Third-party
import pandas as pd
from docx import Document

# Local
from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists
```

## Documentation

### Docstrings
Use Google-style docstrings:

```python
def read_file(path: str) -> Any:
    """
    Read a file and return its contents.
    
    Args:
        path: Path to the file to read
    
    Returns:
        File contents (type depends on file format)
    
    Raises:
        FileNotFoundError: If file does not exist
        UnsupportedFormatError: If file format is not supported
    
    Examples:
        >>> data = read_file("data.csv")
    """
```

### Comments
- Use comments to explain WHY, not WHAT
- Keep comments up-to-date
- Avoid obvious comments

### Type Hints
- Use type hints for all functions
- Use `Optional`, `Union`, `List`, `Dict` from typing
- Use `Any` sparingly

## Debugging

### Print Debugging
```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Using Debugger
```bash
# Run with debugger
python -m pdb script.py

# Or use IDE debugger
# Set breakpoints and run with debugger
```

### Testing with Print
```python
def test_something():
    result = function()
    print(f"Result: {result}")  # Will show with pytest -s
    assert result == expected
```

## Performance

### Profiling
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Optimization
- Profile before optimizing
- Avoid premature optimization
- Focus on algorithmic improvements
- Use built-in functions (they're optimized)

## Troubleshooting

### Import Errors
```bash
# Reinstall package
pip install -e ".[dev]"

# Check Python path
python -c "import sys; print(sys.path)"
```

### Test Failures
```bash
# Run with verbose output
pytest -v

# Show print statements
pytest -s

# Show full traceback
pytest --tb=long

# Run specific test
pytest tests/test_api.py::TestReadFileAPI::test_read_csv_file -v
```

### Type Errors
```bash
# Run type checker
mypy unified_file_reader

# Ignore specific errors
# Add: # type: ignore to line
```

## Continuous Integration

### GitHub Actions
Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - run: pip install -e ".[dev]"
    - run: pytest --cov=unified_file_reader
    - run: black --check unified_file_reader tests
    - run: flake8 unified_file_reader tests
    - run: mypy unified_file_reader
```

## Release Process

### Version Bumping
Update version in:
- `pyproject.toml`
- `unified_file_reader/__init__.py`
- `setup.py`

### Build Distribution
```bash
pip install build
python -m build
```

### Upload to PyPI
```bash
pip install twine
twine upload dist/*
```

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Clean Code in Python](https://www.oreilly.com/library/view/clean-code-in/9781492051565/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

## Getting Help

- Check existing issues
- Read ARCHITECTURE.md
- Review examples/
- Check test files for usage patterns
- Open an issue on GitHub
