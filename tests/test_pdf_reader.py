"""
Tests for PDF reader (pdf_reader.py).

Tests the PDFReader class and its PDF text extraction functionality.
"""

import pytest

from unified_file_reader.readers.pdf_reader import PDFReader


class TestPDFReader:
    """Test suite for PDFReader."""

    @pytest.fixture
    def reader(self):
        """Create a PDFReader instance."""
        return PDFReader()

    def test_can_read_pdf_extension(self, reader):
        """Test that reader recognizes PDF extension."""
        assert reader.can_read(".pdf") is True

    def test_cannot_read_other_extensions(self, reader):
        """Test that reader rejects other extensions."""
        assert reader.can_read(".csv") is False
        assert reader.can_read(".json") is False
        assert reader.can_read(".txt") is False

    def test_case_insensitive_extension(self, reader):
        """Test that extension check is case-insensitive."""
        assert reader.can_read(".PDF") is True
        assert reader.can_read(".Pdf") is True

    def test_read_valid_pdf_file(self, reader, sample_pdf_file):
        """Test reading a valid PDF file."""
        content = reader.read(sample_pdf_file)
        assert isinstance(content, str)
        assert len(content) > 0

    def test_read_nonexistent_file(self, reader, nonexistent_file):
        """Test reading a non-existent file."""
        with pytest.raises(FileNotFoundError):
            reader.read(nonexistent_file)

    def test_read_pdf_with_multiple_pages(self, reader, temp_dir):
        """Test reading PDF with multiple pages."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            pdf_file = f"{temp_dir}/multi_page.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)

            # Page 1
            c.drawString(100, 750, "Page 1 content")
            c.showPage()

            # Page 2
            c.drawString(100, 750, "Page 2 content")
            c.showPage()

            c.save()

            content = reader.read(pdf_file)
            assert isinstance(content, str)
            assert len(content) > 0
        except ImportError:
            pytest.skip("reportlab not installed")

    def test_read_invalid_pdf(self, reader, temp_dir):
        """Test reading invalid PDF raises error."""
        pdf_file = f"{temp_dir}/invalid.pdf"
        with open(pdf_file, "wb") as f:
            f.write(b"This is not a PDF file")

        with pytest.raises(Exception):
            reader.read(pdf_file)
