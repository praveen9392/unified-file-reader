"""
Text file reader implementation.

Reads plain text files and returns content as string.
Follows Single Responsibility Principle (SRP).
"""

from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists


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
            UnicodeDecodeError: If file encoding is not UTF-8
        """
        ensure_file_exists(path)

        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(path, "r", encoding="latin-1") as f:
                return f.read()
