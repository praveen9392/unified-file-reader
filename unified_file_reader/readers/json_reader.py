"""
JSON file reader implementation.

Reads JSON files and returns parsed data.
Follows Single Responsibility Principle (SRP).
"""

import json
import logging
from typing import Any

from unified_file_reader.exceptions import JSONReadException
from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists

logger = logging.getLogger(__name__)


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
            JSONReadException: If file is not valid JSON
            json.JSONDecodeError: Re-raised as cause of JSONReadException (and inherits JSONReadException)
        """
        ensure_file_exists(path)

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.exception("Invalid JSON format in file: %s", path)
            raise JSONReadException(
                message=f"Failed to parse JSON file: {e.msg}",
                file_path=path,
                doc=e.doc,
                pos=e.pos,
            ) from e
        except Exception as e:
            logger.exception("Failed to read JSON file: %s", path)
            raise JSONReadException(f"Failed to read JSON file: {e}", file_path=path) from e
