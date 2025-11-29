"""
CSV file reader implementation.

Reads CSV files and returns data as a list of dictionaries.
Follows Single Responsibility Principle (SRP).
"""

import csv
from typing import Any, Dict, List

from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists


class CSVReader(BaseReader):
    """Reader for CSV (Comma-Separated Values) files."""

    supported_extensions = [".csv"]

    def can_read(self, extension: str) -> bool:
        """Check if this reader supports CSV format."""
        return extension.lower() in self.supported_extensions

    def read(self, path: str) -> List[Dict[str, Any]]:
        """
        Read a CSV file and return as list of dictionaries.

        Args:
            path: Path to CSV file

        Returns:
            List of dictionaries where each dict represents a row

        Raises:
            FileNotFoundError: If file does not exist
            Exception: If file cannot be parsed as CSV
        """
        ensure_file_exists(path)

        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader) if reader else []
        except UnicodeDecodeError:
            # Try with different encoding
            with open(path, newline="", encoding="latin-1") as f:
                reader = csv.DictReader(f)
                return list(reader) if reader else []
