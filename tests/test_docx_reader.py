"""
Tests for DOCX reader (docx_reader.py).

Tests the DOCXReader class and its DOCX text extraction functionality.
"""

import pytest

from unified_file_reader.readers.docx_reader import DOCXReader


class TestDOCXReader:
    """Test suite for DOCXReader."""

    @pytest.fixture
    def reader(self):
        """Create a DOCXReader instance."""
        return DOCXReader()

    def test_can_read_docx_extension(self, reader):
        """Test that reader recognizes DOCX extension."""
        assert reader.can_read(".docx") is True

    def test_cannot_read_other_extensions(self, reader):
        """Test that reader rejects other extensions."""
        assert reader.can_read(".csv") is False
        assert reader.can_read(".json") is False
        assert reader.can_read(".txt") is False

    def test_case_insensitive_extension(self, reader):
        """Test that extension check is case-insensitive."""
        assert reader.can_read(".DOCX") is True
        assert reader.can_read(".Docx") is True

    def test_read_valid_docx_file(self, reader, sample_docx_file):
        """Test reading a valid DOCX file."""
        content = reader.read(sample_docx_file)
        assert isinstance(content, str)
        assert "sample DOCX" in content

    def test_read_docx_with_multiple_paragraphs(self, reader, temp_dir):
        """Test reading DOCX with multiple paragraphs."""
        from docx import Document

        docx_file = f"{temp_dir}/multi_para.docx"
        doc = Document()
        doc.add_paragraph("First paragraph")
        doc.add_paragraph("Second paragraph")
        doc.add_paragraph("Third paragraph")
        doc.save(docx_file)

        content = reader.read(docx_file)
        assert "First paragraph" in content
        assert "Second paragraph" in content
        assert "Third paragraph" in content

    def test_read_docx_with_empty_paragraphs(self, reader, temp_dir):
        """Test reading DOCX with empty paragraphs."""
        from docx import Document

        docx_file = f"{temp_dir}/empty_para.docx"
        doc = Document()
        doc.add_paragraph("First paragraph")
        doc.add_paragraph("")  # Empty paragraph
        doc.add_paragraph("Second paragraph")
        doc.save(docx_file)

        content = reader.read(docx_file)
        # Empty paragraphs should be skipped
        lines = content.split("\n")
        assert len(lines) == 2

    def test_read_nonexistent_file(self, reader, nonexistent_file):
        """Test reading a non-existent file."""
        with pytest.raises(FileNotFoundError):
            reader.read(nonexistent_file)

    def test_read_invalid_docx(self, reader, temp_dir):
        """Test reading invalid DOCX raises error."""
        docx_file = f"{temp_dir}/invalid.docx"
        with open(docx_file, "wb") as f:
            f.write(b"This is not a DOCX file")

        with pytest.raises(Exception):
            reader.read(docx_file)

    def test_read_docx_with_unicode(self, reader, temp_dir):
        """Test reading DOCX with unicode characters."""
        from docx import Document

        docx_file = f"{temp_dir}/unicode.docx"
        doc = Document()
        doc.add_paragraph("Unicode: José, São Paulo, 日本語")
        doc.add_paragraph("Emoji: 🎉 🚀 ✨")
        doc.save(docx_file)

        content = reader.read(docx_file)
        assert "José" in content
        assert "🎉" in content
