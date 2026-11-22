"""
Text file reader implementation.

Reads plain text files and returns content as string.
Follows Single Responsibility Principle (SRP).
"""

import logging

from unified_file_reader.exceptions import TextReadException
from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists

logger = logging.getLogger(__name__)


class TXTReader(BaseReader):
    """Reader for plain text files."""

    supported_extensions = [".txt"]

    def can_read(self, extension: str) -> bool:
        """Check if this reader supports TXT format."""
        return extension.lower() in self.supported_extensions

    def read(self, path: str) -> str:
        """
        Read a text file and return its content.

        Args:
            path: Path to text file

        Returns:
            File content as string

        Raises:
            FileNotFoundError: If file does not exist
            TextReadException: If file cannot be decoded or read
        """
        ensure_file_exists(path)

        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with fallback encoding
            try:
                with open(path, "r", encoding="latin-1") as f:
                    return f.read()
            except Exception as e:
                logger.exception("Failed to decode text file with fallback encoding: %s", path)
                raise TextReadException(f"Failed to read text file: {e}", file_path=path) from e
        except Exception as e:
            logger.exception("Failed to read text file: %s", path)
            raise TextReadException(f"Failed to read text file: {e}", file_path=path) from e
