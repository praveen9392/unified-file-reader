"""
Unified File Reader - A clean, extensible file reader library.

This module provides a unified API for reading multiple file formats
(CSV, JSON, TXT, XLSX, PDF, DOCX) following Clean Architecture principles.
"""

from unified_file_reader.api import read_file
from unified_file_reader.exceptions import (
    ApplicationException,
    BusinessException,
    BusinessValidationException,
    CSVReadException,
    DOCXReadException,
    ExcelReadException,
    FileReaderException,
    FileReadError,
    InfrastructureException,
    JSONReadException,
    PDFReadException,
    ReaderError,
    ResourceNotFoundException,
    TextReadException,
    UnsupportedFormatError,
)

__version__ = "0.2.0"
__author__ = "Praveen"
__all__ = [
    "read_file",
    "ApplicationException",
    "BusinessException",
    "BusinessValidationException",
    "CSVReadException",
    "DOCXReadException",
    "ExcelReadException",
    "FileReaderException",
    "FileReadError",
    "InfrastructureException",
    "JSONReadException",
    "PDFReadException",
    "ReaderError",
    "ResourceNotFoundException",
    "TextReadException",
    "UnsupportedFormatError",
]
