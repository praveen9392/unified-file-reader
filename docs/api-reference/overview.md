# API Reference

## Main Function

### `read_file(path: str) -> Any`
Reads a supported file format from disk and returns its contents.

```python
from unified_file_reader import read_file

data = read_file("dataset.csv")
```

#### Arguments
- **`path`** (`str`): The file path to read (relative or absolute).

#### Returns
- **`List[Dict[str, Any]]`**: For `.csv` and `.xlsx` files (each dict is one row).
- **`Any`** (`dict` / `list`): For `.json` files, preserving the parsed JSON structure.
- **`str`**: For `.txt`, `.pdf`, and `.docx` files, containing the extracted document text.

#### Exceptions
- **`FileNotFoundError`**: Raised if the file does not exist on disk.
- **`ValueError`**: Raised if the path points to a directory instead of a regular file.
- **`UnsupportedFormatError`**: Raised if no reader is registered for the file's extension.
- **`ReaderError`**: Raised if a parser encounters an unrecoverable error reading or decoding the file.

---

## Registry Functions

```python
from unified_file_reader.registry import (
    register_reader,
    get_reader_for_extension,
    get_supported_extensions,
)
```

### `register_reader(reader: BaseReader) -> None`
Registers a new custom reader instance in the global registry. The reader must inherit from `BaseReader`.

### `get_reader_for_extension(extension: str) -> BaseReader`
Returns the reader assigned to the given extension (e.g. `".csv"` or `".pdf"`). Raises `UnsupportedFormatError` if not found.

### `get_supported_extensions() -> List[str]`
Returns a list of all currently supported extensions (e.g. `[".csv", ".json", ".txt", ".xlsx", ".pdf", ".docx"]`).

---

## Exceptions (`unified_file_reader.exceptions`)

- **`ReaderError`**: Base exception class for all reader-related errors.
- **`UnsupportedFormatError`**: Subclass of `ReaderError`. Raised when attempting to read a file with an unrecognized or unsupported extension.
