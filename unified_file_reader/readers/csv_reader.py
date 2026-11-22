"""
CSV file reader implementation.

Reads CSV files and returns data as a list of dictionaries.
Follows Single Responsibility Principle (SRP).
"""

import csv
import logging
from typing import Any, Dict, List

from unified_file_reader.exceptions import CSVReadException
from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists

logger = logging.getLogger(__name__)


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
            CSVReadException: If file cannot be parsed as CSV
        """
        ensure_file_exists(path)

        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader) if reader else []
        except UnicodeDecodeError:
            # Try with fallback encoding
            try:
                with open(path, newline="", encoding="latin-1") as f:
                    reader = csv.DictReader(f)
                    return list(reader) if reader else []
            except Exception as e:
                logger.exception("Failed to parse CSV file with fallback encoding: %s", path)
                raise CSVReadException(f"Failed to read CSV file: {e}", file_path=path) from e
        except Exception as e:
            logger.exception("Failed to parse CSV file: %s", path)
            raise CSVReadException(f"Failed to read CSV file: {e}", file_path=path) from e
