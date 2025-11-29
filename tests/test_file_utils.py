"""
Tests for file utility functions (file_utils.py).

Tests utility functions for file operations.
"""

import os

import pytest

from unified_file_reader.utils.file_utils import (
    ensure_file_exists,
    get_extension,
    get_file_size,
    is_readable,
)


class TestFileUtils:
    """Test suite for file utility functions."""

    def test_get_extension_csv(self):
        """Test extracting CSV extension."""
        ext = get_extension("data.csv")
        assert ext == ".csv"

    def test_get_extension_json(self):
        """Test extracting JSON extension."""
        ext = get_extension("config.json")
        assert ext == ".json"

    def test_get_extension_uppercase(self):
        """Test that extension is lowercase."""
        ext = get_extension("file.CSV")
        assert ext == ".csv"

    def test_get_extension_with_path(self):
        """Test extracting extension from full path."""
        ext = get_extension("/path/to/file.xlsx")
        assert ext == ".xlsx"

    def test_get_extension_no_extension(self):
        """Test file with no extension."""
        ext = get_extension("README")
        assert ext == ""

    def test_get_extension_multiple_dots(self):
        """Test file with multiple dots."""
        ext = get_extension("archive.tar.gz")
        assert ext == ".gz"

    def test_get_extension_empty_path(self):
        """Test that empty path raises ValueError."""
        with pytest.raises(ValueError):
            get_extension("")

    def test_get_extension_invalid_type(self):
        """Test that non-string path raises ValueError."""
        with pytest.raises(ValueError):
            get_extension(None)

    def test_ensure_file_exists_valid(self, temp_dir):
        """Test ensuring file exists with valid file."""
        file_path = os.path.join(temp_dir, "test.txt")
        with open(file_path, "w") as f:
            f.write("test")

        # Should not raise
        ensure_file_exists(file_path)

    def test_ensure_file_exists_nonexistent(self):
        """Test ensuring file exists with non-existent file."""
        with pytest.raises(FileNotFoundError):
            ensure_file_exists("/nonexistent/file.txt")

    def test_ensure_file_exists_directory(self, temp_dir):
        """Test that directory raises ValueError."""
        with pytest.raises(ValueError):
            ensure_file_exists(temp_dir)

    def test_ensure_file_exists_empty_path(self):
        """Test that empty path raises ValueError."""
        with pytest.raises(ValueError):
            ensure_file_exists("")

    def test_ensure_file_exists_invalid_type(self):
        """Test that non-string path raises ValueError."""
        with pytest.raises(ValueError):
            ensure_file_exists(None)

    def test_get_file_size(self, temp_dir):
        """Test getting file size."""
        file_path = os.path.join(temp_dir, "test.txt")
        content = "Hello, World!"
        with open(file_path, "w") as f:
            f.write(content)

        size = get_file_size(file_path)
        assert size == len(content)

    def test_get_file_size_nonexistent(self):
        """Test getting size of non-existent file."""
        with pytest.raises(FileNotFoundError):
            get_file_size("/nonexistent/file.txt")

    def test_is_readable_valid_file(self, temp_dir):
        """Test checking if file is readable."""
        file_path = os.path.join(temp_dir, "test.txt")
        with open(file_path, "w") as f:
            f.write("test")

        assert is_readable(file_path) is True

    def test_is_readable_nonexistent_file(self):
        """Test checking if non-existent file is readable."""
        assert is_readable("/nonexistent/file.txt") is False

    def test_is_readable_directory(self, temp_dir):
        """Test checking if directory is readable."""
        assert is_readable(temp_dir) is False
