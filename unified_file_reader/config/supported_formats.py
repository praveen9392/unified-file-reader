"""
Configuration for supported file formats.

Centralized metadata about all supported file formats.
"""

from typing import Dict, List

# Supported file formats with metadata
SUPPORTED_FORMATS: Dict[str, Dict[str, any]] = {
    ".csv": {
        "name": "Comma-Separated Values",
        "description": "Tabular data in CSV format",
        "return_type": "List[Dict]",
        "reader_class": "CSVReader",
    },
    ".json": {
        "name": "JavaScript Object Notation",
        "description": "Structured data in JSON format",
        "return_type": "Any",
        "reader_class": "JSONReader",
    },
    ".txt": {
        "name": "Plain Text",
        "description": "Plain text file",
        "return_type": "str",
        "reader_class": "TXTReader",
    },
    ".xlsx": {
        "name": "Microsoft Excel",
        "description": "Excel spreadsheet",
        "return_type": "List[Dict]",
        "reader_class": "ExcelReader",
    },
    ".pdf": {
        "name": "Portable Document Format",
        "description": "PDF document",
        "return_type": "str",
        "reader_class": "PDFReader",
    },
    ".docx": {
        "name": "Microsoft Word",
        "description": "Word document",
        "return_type": "str",
        "reader_class": "DOCXReader",
    },
}


def get_supported_extensions() -> List[str]:
    """Get list of all supported file extensions."""
    return list(SUPPORTED_FORMATS.keys())


def is_format_supported(extension: str) -> bool:
    """Check if a file format is supported."""
    return extension.lower() in SUPPORTED_FORMATS


def get_format_info(extension: str) -> Dict[str, any]:
    """Get metadata for a supported format."""
    ext = extension.lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {ext}")
    return SUPPORTED_FORMATS[ext]
