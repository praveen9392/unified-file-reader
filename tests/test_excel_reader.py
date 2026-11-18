"""
Tests for Excel reader (excel_reader.py).

Tests the ExcelReader class and its XLSX parsing functionality.
"""

import pytest

from unified_file_reader.readers.excel_reader import ExcelReader


class TestExcelReader:
    """Test suite for ExcelReader."""

    @pytest.fixture
    def reader(self):
        """Create an ExcelReader instance."""
        return ExcelReader()

    def test_can_read_xlsx_extension(self, reader):
        """Test that reader recognizes XLSX extension."""
        assert reader.can_read(".xlsx") is True

    def test_cannot_read_other_extensions(self, reader):
        """Test that reader rejects other extensions."""
        assert reader.can_read(".csv") is False
        assert reader.can_read(".json") is False
        assert reader.can_read(".txt") is False

    def test_case_insensitive_extension(self, reader):
        """Test that extension check is case-insensitive."""
        assert reader.can_read(".XLSX") is True
        assert reader.can_read(".Xlsx") is True

    def test_read_valid_xlsx_file(self, reader, sample_xlsx_file):
        """Test reading a valid XLSX file."""
        data = reader.read(sample_xlsx_file)
        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0]["name"] == "John"
        assert data[0]["age"] == 30

    def test_read_xlsx_with_multiple_columns(self, reader, temp_dir):
        """Test reading XLSX with multiple columns."""
        import pandas as pd

        xlsx_file = f"{temp_dir}/multi_col.xlsx"
        data = {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "email": ["alice@example.com", "bob@example.com", "charlie@example.com"],
            "age": [25, 30, 35],
        }
        df = pd.DataFrame(data)
        df.to_excel(xlsx_file, index=False)

        result = reader.read(xlsx_file)
        assert len(result) == 3
        assert result[0]["email"] == "alice@example.com"

    def test_read_nonexistent_file(self, reader, nonexistent_file):
        """Test reading a non-existent file."""
        with pytest.raises(FileNotFoundError):
            reader.read(nonexistent_file)

    def test_read_xlsx_with_nan_values(self, reader, temp_dir):
        """Test reading XLSX with NaN values."""
        import numpy as np
        import pandas as pd

        xlsx_file = f"{temp_dir}/with_nan.xlsx"
        data = {
            "name": ["John", "Jane", "Bob"],
            "age": [30, np.nan, 35],
            "city": ["NYC", "LA", np.nan],
        }
        df = pd.DataFrame(data)
        df.to_excel(xlsx_file, index=False)

        result = reader.read(xlsx_file)
        assert len(result) == 3
        # NaN should be converted to None or be NaN
        assert result[1]["age"] is None or pd.isna(result[1]["age"])

    def test_read_empty_xlsx(self, reader, temp_dir):
        """Test reading an empty XLSX file."""
        import pandas as pd

        xlsx_file = f"{temp_dir}/empty.xlsx"
        df = pd.DataFrame()
        df.to_excel(xlsx_file, index=False)

        result = reader.read(xlsx_file)
        assert isinstance(result, list)
