"""
JSON file reader implementation.

Reads JSON files and returns parsed data.
Follows Single Responsibility Principle (SRP).
"""

import json
from typing import Any

from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists


class JSONReader(BaseReader):
    """Reader for JSON (JavaScript Object Notation) files."""

    supported_extensions = [".json"]

    def can_read(self, extension: str) -> bool:
        """Check if this reader supports JSON format."""
        return extension.lower() in self.supported_extensions

    def read(self, path: str) -> Any:
        """
        Read a JSON file and return parsed data.

        Args:
            path: Path to JSON file

        Returns:
            Parsed JSON data (dict, list, or other JSON-compatible type)

        Raises:
            FileNotFoundError: If file does not exist
            json.JSONDecodeError: If file is not valid JSON
        """
        ensure_file_exists(path)

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
