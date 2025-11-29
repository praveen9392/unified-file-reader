# Contributing to Unified File Reader

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Report issues responsibly

## Getting Started

### 1. Fork and Clone
```bash
git clone https://github.com/praveen9392/unified-file-reader.git
cd unified-file-reader
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### 3. Verify Setup
```bash
pytest
black --check unified_file_reader tests
flake8 unified_file_reader tests
mypy unified_file_reader
```

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Follow Clean Code principles
- Keep changes focused and minimal
- Add tests for new functionality
- Update documentation as needed

### 3. Code Quality

#### Format Code
```bash
black unified_file_reader tests
isort unified_file_reader tests
```

#### Run Linter
```bash
flake8 unified_file_reader tests
```

#### Type Checking
```bash
mypy unified_file_reader
```

#### Run Tests
```bash
pytest
pytest --cov=unified_file_reader
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: add support for YAML files"
```

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `chore:` Build, dependencies, etc.

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## Adding a New File Format

### Step 1: Create Reader Class

Create `unified_file_reader/readers/xyz_reader.py`:

```python
"""Reader for XYZ files."""

from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists

class XYZReader(BaseReader):
    """Reader for XYZ format."""
    
    supported_extensions = [".xyz"]
    
    def can_read(self, extension: str) -> bool:
        return extension.lower() in self.supported_extensions
    
    def read(self, path: str):
        ensure_file_exists(path)
        # Implementation here
        pass
```

### Step 2: Register Reader

Update `unified_file_reader/registry.py`:

```python
from unified_file_reader.readers.xyz_reader import XYZReader

_READERS = [
    # ... existing readers ...
    XYZReader(),
]
```

### Step 3: Add Configuration

Update `unified_file_reader/config/supported_formats.py`:

```python
SUPPORTED_FORMATS = {
    # ... existing formats ...
    ".xyz": {
        "name": "XYZ Format",
        "description": "Description of XYZ format",
        "return_type": "Type",
        "reader_class": "XYZReader",
    },
}
```

### Step 4: Write Tests

Create `tests/test_xyz_reader.py`:

```python
"""Tests for XYZ reader."""

import pytest
from unified_file_reader.readers.xyz_reader import XYZReader

class TestXYZReader:
    @pytest.fixture
    def reader(self):
        return XYZReader()
    
    def test_can_read_xyz_extension(self, reader):
        assert reader.can_read(".xyz") is True
    
    def test_read_valid_xyz_file(self, reader, temp_dir):
        # Create test file
        xyz_file = f"{temp_dir}/sample.xyz"
        # Write test data
        
        data = reader.read(xyz_file)
        # Assert expected results
```

### Step 5: Update Documentation

- Update README.md with new format
- Add example usage
- Update ARCHITECTURE.md if needed

### Step 6: Run All Tests

```bash
pytest
pytest --cov=unified_file_reader
```

## Testing Guidelines

### Unit Tests
- Test one thing per test
- Use descriptive test names
- Use fixtures for setup
- Mock external dependencies

### Integration Tests
- Test real file reading
- Use sample files in `tests/resources/`
- Test error cases

### Test Coverage
- Aim for >90% coverage
- All public APIs must be tested
- Test edge cases and error conditions

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=unified_file_reader

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::TestReadFileAPI::test_read_csv_file

# Run with verbose output
pytest -v

# Run with output
pytest -s
```

## Documentation Guidelines

### Code Documentation
- Add docstrings to all public functions/classes
- Use Google-style docstrings
- Include Args, Returns, Raises sections
- Add examples for complex functions

Example:
```python
def read_file(path: str) -> Any:
    """
    Read a file and return its contents.
    
    Supported formats: CSV, JSON, TXT, XLSX, PDF, DOCX
    
    Args:
        path: Path to the file to read
    
    Returns:
        File contents (type depends on file format)
    
    Raises:
        FileNotFoundError: If file does not exist
        UnsupportedFormatError: If file format is not supported
    
    Examples:
        >>> data = read_file("data.csv")
        >>> config = read_file("config.json")
    """
```

### README Updates
- Keep examples clear and concise
- Update feature list
- Add new format to supported formats table

### Architecture Documentation
- Update ARCHITECTURE.md for major changes
- Add diagrams if helpful
- Document design decisions

## Pull Request Process

1. **Ensure Tests Pass**
   ```bash
   pytest
   pytest --cov=unified_file_reader
   ```

2. **Format Code**
   ```bash
   black unified_file_reader tests
   isort unified_file_reader tests
   ```

3. **Check Linting**
   ```bash
   flake8 unified_file_reader tests
   mypy unified_file_reader
   ```

4. **Write PR Description**
   - Describe changes clearly
   - Reference related issues
   - Include examples if applicable

5. **Wait for Review**
   - Respond to feedback
   - Make requested changes
   - Re-run tests after changes

## Reporting Issues

### Bug Reports
Include:
- Python version
- OS and version
- Minimal code to reproduce
- Expected vs actual behavior
- Error traceback

### Feature Requests
Include:
- Use case description
- Why it's needed
- Proposed solution (if any)
- Examples

## Style Guide

### Python Style
- Follow PEP 8
- Use Black for formatting
- Use isort for imports
- Use type hints

### Naming Conventions
- Classes: PascalCase (e.g., `CSVReader`)
- Functions: snake_case (e.g., `read_file`)
- Constants: UPPER_SNAKE_CASE (e.g., `SUPPORTED_FORMATS`)
- Private: _leading_underscore (e.g., `_internal_function`)

### Imports
- Group: standard library, third-party, local
- Sort alphabetically within groups
- Use absolute imports

```python
import json
import os
from typing import Any, Dict, List

import pandas as pd
from docx import Document

from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists
```

## Performance Considerations

- Avoid unnecessary imports
- Use generators for large data
- Cache when appropriate
- Profile before optimizing

## Security Considerations

- Validate file paths
- Handle untrusted input safely
- Use safe parsing methods
- Avoid arbitrary code execution

## Questions?

- Check existing issues and discussions
- Read ARCHITECTURE.md
- Ask in pull request comments
- Open a discussion issue

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md
- Release notes
- GitHub contributors page

Thank you for contributing! 🎉
