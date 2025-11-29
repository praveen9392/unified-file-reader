"""
DOCX file reader implementation.

Reads DOCX files and extracts text content.
Follows Single Responsibility Principle (SRP).
"""

from docx import Document

from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists


class DOCXReader(BaseReader):
    """Reader for DOCX (Microsoft Word) files."""

    supported_extensions = [".docx"]

    def can_read(self, extension: str) -> bool:
        """Check if this reader supports DOCX format."""
        return extension.lower() in self.supported_extensions

    def read(self, path: str) -> str:
        """
        Read a DOCX file and extract all paragraph text.

        Args:
            path: Path to DOCX file

        Returns:
            Extracted text from all paragraphs, joined with newlines

        Raises:
            FileNotFoundError: If file does not exist
            Exception: If file cannot be parsed as DOCX
        """
        ensure_file_exists(path)

        try:
            doc = Document(path)
            paragraphs = [p.text for p in doc.paragraphs if p.text]
            return "\n".join(paragraphs)
        except Exception as e:
            raise Exception(f"Failed to read DOCX file: {str(e)}")
