"""
PDF file reader implementation.

Reads PDF files and extracts text content.
Follows Single Responsibility Principle (SRP).
"""

from pypdf import PdfReader

from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.utils.file_utils import ensure_file_exists


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
            Exception: If file cannot be parsed as PDF
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
            raise Exception(f"Failed to read PDF file: {str(e)}")
