"""
Tests for JSON reader (json_reader.py).

Tests the JSONReader class and its JSON parsing functionality.
"""

import json

import pytest

from unified_file_reader.readers.json_reader import JSONReader


class TestJSONReader:
    """Test suite for JSONReader."""

    @pytest.fixture
    def reader(self):
        """Create a JSONReader instance."""
        return JSONReader()

    def test_can_read_json_extension(self, reader):
        """Test that reader recognizes JSON extension."""
        assert reader.can_read(".json") is True

    def test_cannot_read_other_extensions(self, reader):
        """Test that reader rejects other extensions."""
        assert reader.can_read(".csv") is False
        assert reader.can_read(".txt") is False
        assert reader.can_read(".xlsx") is False

    def test_case_insensitive_extension(self, reader):
        """Test that extension check is case-insensitive."""
        assert reader.can_read(".JSON") is True
        assert reader.can_read(".Json") is True

    def test_read_valid_json_object(self, reader, sample_json_file):
        """Test reading a valid JSON object."""
        data = reader.read(sample_json_file)
        assert isinstance(data, dict)
        assert data["name"] == "John"
        assert data["age"] == 30

    def test_read_json_array(self, reader, temp_dir):
        """Test reading a JSON array."""
        json_file = f"{temp_dir}/array.json"
        data = [{"id": 1}, {"id": 2}, {"id": 3}]
        with open(json_file, "w") as f:
            json.dump(data, f)

        result = reader.read(json_file)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_read_json_with_nested_structure(self, reader, temp_dir):
        """Test reading JSON with nested objects."""
        json_file = f"{temp_dir}/nested.json"
        data = {
            "user": {"name": "John", "address": {"city": "NYC"}},
            "items": [1, 2, 3],
        }
        with open(json_file, "w") as f:
            json.dump(data, f)

        result = reader.read(json_file)
        assert result["user"]["address"]["city"] == "NYC"

    def test_read_invalid_json(self, reader, temp_dir):
        """Test reading invalid JSON raises error."""
        json_file = f"{temp_dir}/invalid.json"
        with open(json_file, "w") as f:
            f.write("{invalid json}")

        with pytest.raises(json.JSONDecodeError):
            reader.read(json_file)

    def test_read_nonexistent_file(self, reader, nonexistent_file):
        """Test reading a non-existent file."""
        with pytest.raises(FileNotFoundError):
            reader.read(nonexistent_file)

    def test_read_json_with_unicode(self, reader, temp_dir):
        """Test reading JSON with unicode characters."""
        json_file = f"{temp_dir}/unicode.json"
        data = {"name": "José", "city": "São Paulo", "emoji": "🎉"}
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        result = reader.read(json_file)
        assert result["emoji"] == "🎉"
