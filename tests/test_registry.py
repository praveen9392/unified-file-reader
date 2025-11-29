"""
Tests for the reader registry (registry.py).

Tests the registry functionality for managing and retrieving readers.
"""

import pytest

from unified_file_reader.interfaces.base_reader import BaseReader
from unified_file_reader.registry import (
    get_all_readers,
    get_reader_for_extension,
    get_supported_extensions,
    register_reader,
)


class DummyReader(BaseReader):
    """Dummy reader for testing custom registration."""

    supported_extensions = [".dummy"]

    def can_read(self, extension: str) -> bool:
        return extension.lower() in self.supported_extensions

    def read(self, path: str):
        return "dummy content"


class TestRegistry:
    """Test suite for reader registry."""

    def test_get_reader_for_csv(self):
        """Test getting CSV reader."""
        reader = get_reader_for_extension(".csv")
        assert reader is not None
        assert reader.can_read(".csv")

    def test_get_reader_for_json(self):
        """Test getting JSON reader."""
        reader = get_reader_for_extension(".json")
        assert reader is not None
        assert reader.can_read(".json")

    def test_get_reader_for_txt(self):
        """Test getting TXT reader."""
        reader = get_reader_for_extension(".txt")
        assert reader is not None
        assert reader.can_read(".txt")

    def test_get_reader_for_xlsx(self):
        """Test getting XLSX reader."""
        reader = get_reader_for_extension(".xlsx")
        assert reader is not None
        assert reader.can_read(".xlsx")

    def test_get_reader_for_pdf(self):
        """Test getting PDF reader."""
        reader = get_reader_for_extension(".pdf")
        assert reader is not None
        assert reader.can_read(".pdf")

    def test_get_reader_for_docx(self):
        """Test getting DOCX reader."""
        reader = get_reader_for_extension(".docx")
        assert reader is not None
        assert reader.can_read(".docx")

    def test_get_reader_for_unsupported_format(self):
        """Test getting reader for unsupported format."""
        reader = get_reader_for_extension(".xyz")
        assert reader is None

    def test_case_insensitive_lookup(self):
        """Test that reader lookup is case-insensitive."""
        reader1 = get_reader_for_extension(".CSV")
        reader2 = get_reader_for_extension(".csv")
        assert reader1 is not None
        assert reader1 == reader2

    def test_get_all_readers(self):
        """Test getting all registered readers."""
        readers = get_all_readers()
        assert isinstance(readers, list)
        assert len(readers) >= 6  # At least 6 default readers

    def test_get_supported_extensions(self):
        """Test getting list of supported extensions."""
        extensions = get_supported_extensions()
        assert isinstance(extensions, list)
        assert ".csv" in extensions
        assert ".json" in extensions
        assert ".txt" in extensions
        assert ".xlsx" in extensions
        assert ".pdf" in extensions
        assert ".docx" in extensions

    def test_register_custom_reader(self):
        """Test registering a custom reader."""
        dummy = DummyReader()
        initial_count = len(get_all_readers())

        register_reader(dummy)

        assert len(get_all_readers()) == initial_count + 1
        reader = get_reader_for_extension(".dummy")
        assert reader is not None
        assert reader.can_read(".dummy")

    def test_register_invalid_reader(self):
        """Test that registering non-BaseReader raises error."""

        class InvalidReader:
            pass

        with pytest.raises(TypeError):
            register_reader(InvalidReader())

    def test_all_readers_implement_base_reader(self):
        """Test that all registered readers implement BaseReader."""
        readers = get_all_readers()
        for reader in readers:
            assert isinstance(reader, BaseReader)
