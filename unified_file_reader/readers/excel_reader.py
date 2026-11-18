"""
Excel file reader implementation.

Reads XLSX files and returns data as list of dictionaries.
Follows Single Responsibility Principle (SRP).
"""

from typing import Any, Dict, List

import pandas as pd

from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists


class ExcelReader(BaseReader):
    """Reader for Excel (XLSX) files."""

    supported_extensions = [".xlsx"]

    def can_read(self, extension: str) -> bool:
        """Check if this reader supports XLSX format."""
        return extension.lower() in self.supported_extensions

    def read(self, path: str) -> List[Dict[str, Any]]:
        """
        Read an Excel file and return as list of dictionaries.

        Args:
            path: Path to Excel file

        Returns:
            List of dictionaries where each dict represents a row

        Raises:
            FileNotFoundError: If file does not exist
            Exception: If file cannot be parsed as Excel
        """
        ensure_file_exists(path)

        try:
            df = pd.read_excel(path)
            # Handle NaN values by converting to None
            df = df.where(pd.notna(df), None)
            records = df.to_dict(orient="records")
            return list(records) if isinstance(records, list) else []
        except Exception as e:
            raise Exception(f"Failed to read Excel file: {str(e)}")
