"""
PDF file reader implementation.

Reads PDF files and extracts text content.
Follows Single Responsibility Principle (SRP).
"""

import logging
from pypdf import PdfReader

from unified_file_reader.exceptions import PDFReadException
from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists

logger = logging.getLogger(__name__)


class PDFReader(BaseReader):
    """Reader for PDF (Portable Document Format) files."""

    supported_extensions = [".pdf"]

    def can_read(self, extension: str) -> bool:
        """Check if this reader supports PDF format."""
        return extension.lower() in self.supported_extensions

    def read(self, path: str) -> str:
        """
        Read a PDF file and extract all text content.

        Args:
            path: Path to PDF file

        Returns:
            Extracted text from all pages, joined with newlines

        Raises:
            FileNotFoundError: If file does not exist
            PDFReadException: If file cannot be parsed as PDF
        """
        ensure_file_exists(path)

        try:
            reader = PdfReader(path)
            text_parts = []

            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    text_parts.append(text)

            return "\n".join(text_parts)
        except Exception as e:
            logger.exception("Failed to parse PDF file: %s", path)
            raise PDFReadException(f"Failed to read PDF file: {e}", file_path=path) from e
