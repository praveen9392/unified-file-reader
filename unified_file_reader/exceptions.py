"""
Custom exceptions for the unified file reader library.

Follows Clean Code principle: use specific, meaningful exceptions
for better error handling and debugging.
"""


class ReaderError(Exception):
    """Base exception for all reader-related errors."""

    pass


class UnsupportedFormatError(ReaderError):
    """Raised when attempting to read an unsupported file format."""

    pass


class FileReadError(ReaderError):
    """Raised when an error occurs while reading a file."""

    pass
