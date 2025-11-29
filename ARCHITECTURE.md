# Architecture Documentation

## Overview

Unified File Reader is built using **Clean Architecture** and **Clean Code** principles. This document explains the architectural design and how components interact.

## Architectural Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    USE-CASE LAYER (API)                     │
│                        api.py                               │
│                    read_file(path)                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              INTERFACE LAYER (ABSTRACTIONS)                 │
│                  interfaces/base_reader.py                  │
│                    BaseReader (ABC)                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   REGISTRY   │  │  UTILITIES   │  │   CONFIG     │
│ registry.py  │  │ file_utils.py│  │supported_    │
│              │  │              │  │formats.py    │
└──────────────┘  └──────────────┘  └──────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│          INFRASTRUCTURE LAYER (IMPLEMENTATIONS)             │
│                    readers/                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │CSV       │ │JSON      │ │TXT       │ │EXCEL     │      │
│  │Reader    │ │Reader    │ │Reader    │ │Reader    │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│  ┌──────────┐ ┌──────────┐                                 │
│  │PDF       │ │DOCX      │                                 │
│  │Reader    │ │Reader    │                                 │
│  └──────────┘ └──────────┘                                 │
└─────────────────────────────────────────────────────────────┘
```

## Design Principles

### 1. Single Responsibility Principle (SRP)

Each class has a single, well-defined responsibility:

- **CSVReader**: Reads CSV files only
- **JSONReader**: Reads JSON files only
- **TXTReader**: Reads text files only
- **ExcelReader**: Reads Excel files only
- **PDFReader**: Reads PDF files only
- **DOCXReader**: Reads DOCX files only
- **api.py**: Orchestrates file reading (use-case logic)
- **registry.py**: Maps extensions to readers
- **file_utils.py**: Provides common file operations

### 2. Open/Closed Principle (OCP)

The system is:
- **Open for extension**: Add new readers without modifying existing code
- **Closed for modification**: Core API remains stable

Example: To add YAML support:
```python
# Create new reader
class YAMLReader(BaseReader):
    supported_extensions = [".yaml", ".yml"]
    def can_read(self, extension: str) -> bool:
        return extension in self.supported_extensions
    def read(self, path: str):
        # Implementation

# Register it
from unified_file_reader.registry import register_reader
register_reader(YAMLReader())

# Use it immediately
from unified_file_reader import read_file
data = read_file("config.yaml")
```

### 3. Liskov Substitution Principle (LSP)

All readers are interchangeable:
```python
def process_file(reader: BaseReader, path: str):
    return reader.read(path)

# Works with any reader
process_file(CSVReader(), "data.csv")
process_file(JSONReader(), "config.json")
process_file(PDFReader(), "document.pdf")
```

### 4. Interface Segregation Principle (ISP)

`BaseReader` interface is minimal and focused:
```python
class BaseReader(ABC):
    @abstractmethod
    def can_read(self, extension: str) -> bool:
        pass
    
    @abstractmethod
    def read(self, path: str) -> Any:
        pass
```

No unnecessary methods or dependencies.

### 5. Dependency Inversion Principle (DIP)

High-level modules depend on abstractions, not concrete implementations:

```python
# ✅ GOOD: api.py depends on BaseReader (abstraction)
def read_file(path: str) -> Any:
    reader = get_reader_for_extension(extension)  # Returns BaseReader
    return reader.read(path)

# ❌ BAD: Direct dependency on concrete classes
def read_file(path: str) -> Any:
    if extension == ".csv":
        return CSVReader().read(path)
    elif extension == ".json":
        return JSONReader().read(path)
    # ... many more conditions
```

## Module Responsibilities

### api.py (Use-Case Layer)
- **Responsibility**: Orchestrate file reading operations
- **Dependencies**: registry, file_utils, exceptions
- **Public API**: `read_file(path)`
- **Principles**: DIP, SRP

### registry.py (Service Locator)
- **Responsibility**: Map file extensions to appropriate readers
- **Dependencies**: All reader implementations
- **Functions**: 
  - `get_reader_for_extension()`
  - `register_reader()`
  - `get_all_readers()`
  - `get_supported_extensions()`
- **Principles**: OCP, DIP

### interfaces/base_reader.py (Abstraction)
- **Responsibility**: Define reader contract
- **Dependencies**: None
- **Methods**: `can_read()`, `read()`
- **Principles**: ISP, LSP

### readers/*.py (Implementations)
- **Responsibility**: Read specific file format
- **Dependencies**: BaseReader, file_utils
- **Principles**: SRP, LSP

### utils/file_utils.py (Utilities)
- **Responsibility**: Provide common file operations
- **Dependencies**: None
- **Functions**: `get_extension()`, `ensure_file_exists()`, `get_file_size()`, `is_readable()`
- **Principles**: DRY, SRP

### config/supported_formats.py (Configuration)
- **Responsibility**: Centralize format metadata
- **Dependencies**: None
- **Principles**: SRP

### exceptions.py (Error Handling)
- **Responsibility**: Define custom exceptions
- **Dependencies**: None
- **Principles**: Clean Code (meaningful exceptions)

## Data Flow

### Reading a File

```
User calls read_file("data.csv")
    ↓
api.py extracts extension ".csv"
    ↓
registry.get_reader_for_extension(".csv")
    ↓
Returns CSVReader instance
    ↓
CSVReader.read("data.csv")
    ↓
file_utils.ensure_file_exists() validates file
    ↓
csv.DictReader() parses content
    ↓
Returns List[Dict] to user
```

## Extensibility Example: Adding YAML Support

### Step 1: Create Reader
```python
# unified_file_reader/readers/yaml_reader.py
import yaml
from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists

class YAMLReader(BaseReader):
    supported_extensions = [".yaml", ".yml"]
    
    def can_read(self, extension: str) -> bool:
        return extension.lower() in self.supported_extensions
    
    def read(self, path: str):
        ensure_file_exists(path)
        with open(path, 'r') as f:
            return yaml.safe_load(f)
```

### Step 2: Register Reader
```python
# unified_file_reader/registry.py
from unified_file_reader.readers.yaml_reader import YAMLReader

_READERS = [
    # ... existing readers ...
    YAMLReader(),
]
```

### Step 3: Add Tests
```python
# tests/test_yaml_reader.py
def test_read_yaml_file():
    reader = YAMLReader()
    data = reader.read("config.yaml")
    assert isinstance(data, dict)
```

### Step 4: Use It
```python
from unified_file_reader import read_file

config = read_file("config.yaml")
```

**No changes to api.py or other readers needed!**

## Testing Strategy

### Unit Tests
- Test each reader independently
- Test utility functions
- Test registry functionality

### Integration Tests
- Test read_file() with different formats
- Test error handling
- Test edge cases

### Test Organization
```
tests/
├── conftest.py           # Shared fixtures
├── test_api.py           # API integration tests
├── test_csv_reader.py    # CSV reader unit tests
├── test_json_reader.py   # JSON reader unit tests
├── test_txt_reader.py    # TXT reader unit tests
├── test_excel_reader.py  # Excel reader unit tests
├── test_pdf_reader.py    # PDF reader unit tests
├── test_docx_reader.py   # DOCX reader unit tests
├── test_registry.py      # Registry tests
└── test_file_utils.py    # Utility function tests
```

## Error Handling

Custom exceptions provide meaningful error messages:

```python
class ReaderError(Exception):
    """Base exception for all reader-related errors."""

class UnsupportedFormatError(ReaderError):
    """Raised when attempting to read an unsupported file format."""

class FileReadError(ReaderError):
    """Raised when an error occurs while reading a file."""
```

Usage:
```python
try:
    data = read_file("file.xyz")
except UnsupportedFormatError as e:
    print(f"Format not supported: {e}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ReaderError as e:
    print(f"Reading error: {e}")
```

## Performance Considerations

1. **Lazy Loading**: Readers are instantiated once and reused
2. **Minimal Dependencies**: Each reader imports only necessary libraries
3. **Efficient Parsing**: Uses optimized libraries (pandas, pypdf, python-docx)
4. **Memory Management**: Streams large files when possible

## Future Enhancements

1. **Async Readers**: Add async/await support for large files
2. **Plugin System**: Dynamic reader discovery via entry_points
3. **Caching**: Cache parsed files for repeated reads
4. **Streaming**: Support streaming for very large files
5. **Custom Serializers**: Allow custom output formats
6. **Validation**: Add schema validation for structured formats

## Summary

This architecture ensures:
- ✅ Easy to understand and maintain
- ✅ Easy to test and debug
- ✅ Easy to extend with new formats
- ✅ Follows SOLID principles
- ✅ Production-ready and scalable
