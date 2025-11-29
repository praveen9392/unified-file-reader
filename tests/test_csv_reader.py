"""
Tests for CSV reader (csv_reader.py).

Tests the CSVReader class and its CSV parsing functionality.
"""

import pytest

from unified_file_reader.readers.csv_reader import CSVReader


class TestCSVReader:
    """Test suite for CSVReader."""

    @pytest.fixture
    def reader(self):
        """Create a CSVReader instance."""
        return CSVReader()

    def test_can_read_csv_extension(self, reader):
        """Test that reader recognizes CSV extension."""
        assert reader.can_read(".csv") is True

    def test_cannot_read_other_extensions(self, reader):
        """Test that reader rejects other extensions."""
        assert reader.can_read(".json") is False
        assert reader.can_read(".txt") is False
        assert reader.can_read(".xlsx") is False

    def test_case_insensitive_extension(self, reader):
        """Test that extension check is case-insensitive."""
        assert reader.can_read(".CSV") is True
        assert reader.can_read(".Csv") is True

    def test_read_valid_csv(self, reader, sample_csv_file):
        """Test reading a valid CSV file."""
        data = reader.read(sample_csv_file)
        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0]["name"] == "John"
        assert data[1]["name"] == "Jane"
        assert data[2]["name"] == "Bob"

    def test_read_csv_with_different_encoding(self, reader, temp_dir):
        """Test reading CSV with non-UTF-8 encoding."""
        csv_file = f"{temp_dir}/latin1.csv"
        # Write with latin-1 encoding
        with open(csv_file, "w", encoding="latin-1") as f:
            f.write("name,city\n")
            f.write("José,São Paulo\n")

        data = reader.read(csv_file)
        assert isinstance(data, list)
        assert len(data) == 1

    def test_read_nonexistent_file(self, reader, nonexistent_file):
        """Test reading a non-existent file."""
        with pytest.raises(FileNotFoundError):
            reader.read(nonexistent_file)

    def test_read_empty_csv(self, reader, temp_dir):
        """Test reading an empty CSV file."""
        csv_file = f"{temp_dir}/empty.csv"
        with open(csv_file, "w") as f:
            f.write("")

        data = reader.read(csv_file)
        assert isinstance(data, list)
        assert len(data) == 0

    def test_read_csv_with_special_characters(self, reader, temp_dir):
        """Test reading CSV with special characters."""
        csv_file = f"{temp_dir}/special.csv"
        with open(csv_file, "w", newline="") as f:
            f.write("name,description\n")
            f.write('John,"A ""quoted"" value"\n')
            f.write('Jane,"Value with, comma"\n')

        data = reader.read(csv_file)
        assert len(data) == 2
        assert "quoted" in data[0]["description"]
