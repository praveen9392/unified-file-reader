"""
Public API for the unified file reader library.

This is the use-case layer - the single entry point for all file reading operations.
Follows Clean Architecture principles:
- High-level module (API) depends on abstractions (BaseReader, registry)
- Not on concrete implementations
- Format-agnostic and extensible
"""

import logging
from typing import Any

from unified_file_reader.exceptions import ApplicationException, UnsupportedFormatError
from unified_file_reader.registry import get_reader_for_extension
from unified_file_reader.utils.file_utils import get_extension

logger = logging.getLogger(__name__)


def read_file(path: str) -> Any:
    """
    Read a file and return its contents.

    This is the main public API. It automatically detects the file format
    and uses the appropriate reader to parse it.

    Supported formats:
    - CSV (.csv) -> List[Dict]
    - JSON (.json) -> Any
    - TXT (.txt) -> str
    - Excel (.xlsx) -> List[Dict]
    - PDF (.pdf) -> str
    - DOCX (.docx) -> str

    Args:
        path: Path to the file to read

    Returns:
        File contents (type depends on file format)

    Raises:
        FileNotFoundError: If file does not exist
        UnsupportedFormatError: If file format is not supported
        Exception: If file cannot be read or parsed

    Examples:
        >>> data = read_file("data.csv")
        >>> config = read_file("config.json")
        >>> text = read_file("document.pdf")
    """
    try:
        # Extract file extension
        extension = get_extension(path)
        logger.debug(f"Reading file: {path} (extension: {extension})")

        # Get appropriate reader
        reader = get_reader_for_extension(extension)

        if not reader:
            supported = [".csv", ".json", ".txt", ".xlsx", ".pdf", ".docx"]
            raise UnsupportedFormatError(
                f"Unsupported file format: '{extension}'. "
                f"Supported formats: {', '.join(supported)}",
                extension=extension,
            )

        # Read file using appropriate reader
        logger.debug(f"Using reader: {reader.__class__.__name__}")
        result = reader.read(path)
        logger.debug(f"Successfully read file: {path}")

        return result

    except (UnsupportedFormatError, FileNotFoundError, ApplicationException):
        raise
    except Exception as e:
        logger.error(f"Error reading file {path}: {str(e)}")
        raise
