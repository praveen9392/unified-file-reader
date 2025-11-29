"""
Tests for TXT reader (txt_reader.py).

Tests the TXTReader class and its text file reading functionality.
"""

import pytest

from unified_file_reader.readers.txt_reader import TXTReader


class TestTXTReader:
    """Test suite for TXTReader."""

    @pytest.fixture
    def reader(self):
        """Create a TXTReader instance."""
        return TXTReader()

    def test_can_read_txt_extension(self, reader):
        """Test that reader recognizes TXT extension."""
        assert reader.can_read(".txt") is True

    def test_cannot_read_other_extensions(self, reader):
        """Test that reader rejects other extensions."""
        assert reader.can_read(".csv") is False
        assert reader.can_read(".json") is False
        assert reader.can_read(".xlsx") is False

    def test_case_insensitive_extension(self, reader):
        """Test that extension check is case-insensitive."""
        assert reader.can_read(".TXT") is True
        assert reader.can_read(".Txt") is True

    def test_read_valid_txt_file(self, reader, sample_txt_file):
        """Test reading a valid text file."""
        content = reader.read(sample_txt_file)
        assert isinstance(content, str)
        assert "sample text file" in content
        assert "multiple lines" in content

    def test_read_empty_txt_file(self, reader, temp_dir):
        """Test reading an empty text file."""
        txt_file = f"{temp_dir}/empty.txt"
        with open(txt_file, "w") as f:
            f.write("")

        content = reader.read(txt_file)
        assert isinstance(content, str)
        assert len(content) == 0

    def test_read_txt_with_special_characters(self, reader, temp_dir):
        """Test reading text with special characters."""
        txt_file = f"{temp_dir}/special.txt"
        with open(txt_file, "w") as f:
            f.write("Special chars: @#$%^&*()\n")
            f.write("Symbols: ™®©\n")

        content = reader.read(txt_file)
        assert "@#$%^&*()" in content

    def test_read_txt_with_unicode(self, reader, temp_dir):
        """Test reading text with unicode characters."""
        txt_file = f"{temp_dir}/unicode.txt"
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("Unicode: José, São Paulo, 日本語\n")
            f.write("Emoji: 🎉 🚀 ✨\n")

        content = reader.read(txt_file)
        assert "José" in content
        assert "🎉" in content

    def test_read_txt_with_different_encoding(self, reader, temp_dir):
        """Test reading text with non-UTF-8 encoding."""
        txt_file = f"{temp_dir}/latin1.txt"
        with open(txt_file, "w", encoding="latin-1") as f:
            f.write("Latin-1 text: café\n")

        content = reader.read(txt_file)
        assert isinstance(content, str)

    def test_read_nonexistent_file(self, reader, nonexistent_file):
        """Test reading a non-existent file."""
        with pytest.raises(FileNotFoundError):
            reader.read(nonexistent_file)

    def test_read_large_txt_file(self, reader, temp_dir):
        """Test reading a large text file."""
        txt_file = f"{temp_dir}/large.txt"
        with open(txt_file, "w") as f:
            for i in range(10000):
                f.write(f"Line {i}: This is a test line.\n")

        content = reader.read(txt_file)
        assert isinstance(content, str)
        assert "Line 0" in content
        assert "Line 9999" in content
