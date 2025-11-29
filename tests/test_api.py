"""
Tests for the public API (api.py).

Tests the main read_file() function and its behavior with different file formats.
"""

import pytest

from unified_file_reader import read_file
from unified_file_reader.exceptions import UnsupportedFormatError


class TestReadFileAPI:
    """Test suite for read_file() function."""

    def test_read_csv_file(self, sample_csv_file):
        """Test reading a CSV file."""
        data = read_file(sample_csv_file)
        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0]["name"] == "John"
        assert data[0]["age"] == "30"

    def test_read_json_file(self, sample_json_file):
        """Test reading a JSON file."""
        data = read_file(sample_json_file)
        assert isinstance(data, dict)
        assert data["name"] == "John"
        assert data["age"] == 30
        assert "hobbies" in data

    def test_read_txt_file(self, sample_txt_file):
        """Test reading a TXT file."""
        content = read_file(sample_txt_file)
        assert isinstance(content, str)
        assert "sample text file" in content
        assert "multiple lines" in content

    def test_read_xlsx_file(self, sample_xlsx_file):
        """Test reading an XLSX file."""
        data = read_file(sample_xlsx_file)
        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0]["name"] == "John"
        assert data[0]["age"] == 30

    def test_read_pdf_file(self, sample_pdf_file):
        """Test reading a PDF file."""
        content = read_file(sample_pdf_file)
        assert isinstance(content, str)
        assert "sample PDF" in content

    def test_read_docx_file(self, sample_docx_file):
        """Test reading a DOCX file."""
        content = read_file(sample_docx_file)
        assert isinstance(content, str)
        assert "sample DOCX" in content

    def test_unsupported_format(self, temp_dir):
        """Test reading an unsupported file format."""
        unsupported_file = f"{temp_dir}/file.xyz"
        with open(unsupported_file, "w") as f:
            f.write("content")

        with pytest.raises(UnsupportedFormatError):
            read_file(unsupported_file)

    def test_nonexistent_file(self, nonexistent_file):
        """Test reading a non-existent file."""
        with pytest.raises(FileNotFoundError):
            read_file(nonexistent_file)

    def test_case_insensitive_extension(self, temp_dir):
        """Test that file extension detection is case-insensitive."""
        # Create a file with uppercase extension
        json_file = f"{temp_dir}/sample.JSON"
        with open(json_file, "w") as f:
            f.write('{"key": "value"}')

        data = read_file(json_file)
        assert isinstance(data, dict)
        assert data["key"] == "value"

    def test_empty_csv_file(self, temp_dir):
        """Test reading an empty CSV file."""
        csv_file = f"{temp_dir}/empty.csv"
        with open(csv_file, "w") as f:
            f.write("")

        data = read_file(csv_file)
        assert isinstance(data, list)
        assert len(data) == 0

    def test_csv_with_headers_only(self, temp_dir):
        """Test reading a CSV file with only headers."""
        csv_file = f"{temp_dir}/headers_only.csv"
        with open(csv_file, "w") as f:
            f.write("name,age,city\n")

        data = read_file(csv_file)
        assert isinstance(data, list)
        assert len(data) == 0
