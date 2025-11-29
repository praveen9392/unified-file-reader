"""
Reader registry - maps file extensions to reader implementations.

Implements Dependency Inversion Principle (DIP):
- High-level API depends on abstractions (BaseReader)
- Not on concrete implementations
- Easy to add new readers without modifying API

Implements Open/Closed Principle (OCP):
- Open for extension (add new readers)
- Closed for modification (API stays stable)
"""

from typing import List, Optional

from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.readers.csv_reader import CSVReader
from unified_file_reader.readers.docx_reader import DOCXReader
from unified_file_reader.readers.excel_reader import ExcelReader
from unified_file_reader.readers.json_reader import JSONReader
from unified_file_reader.readers.pdf_reader import PDFReader
from unified_file_reader.readers.txt_reader import TXTReader

# Registry of all available readers
_READERS: List[BaseReader] = [
    CSVReader(),
    JSONReader(),
    TXTReader(),
    ExcelReader(),
    PDFReader(),
    DOCXReader(),
]


def get_reader_for_extension(extension: str) -> Optional[BaseReader]:
    """
    Get the appropriate reader for a file extension.

    Args:
        extension: File extension (e.g., ".csv")

    Returns:
        Reader instance if found, None otherwise
    """
    ext = extension.lower()
    for reader in _READERS:
        if reader.can_read(ext):
            return reader
    return None


def register_reader(reader: BaseReader) -> None:
    """
    Register a new reader in the registry.

    This allows extending the library with custom readers without
    modifying the core API.

    Args:
        reader: Reader instance implementing BaseReader interface
    """
    if not isinstance(reader, BaseReader):
        raise TypeError("Reader must implement BaseReader interface")
    _READERS.append(reader)


def get_all_readers() -> List[BaseReader]:
    """Get list of all registered readers."""
    return _READERS.copy()


def get_supported_extensions() -> List[str]:
    """Get list of all supported file extensions."""
    extensions = set()
    for reader in _READERS:
        if hasattr(reader, "supported_extensions"):
            extensions.update(reader.supported_extensions)
    return sorted(list(extensions))
