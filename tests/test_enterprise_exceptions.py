"""
Unit tests for enterprise exception hierarchy and behavior.
"""

import pytest

from unified_file_reader.exceptions import (
    ApplicationException,
    BusinessException,
    BusinessValidationException,
    CSVReadException,
    DOCXReadException,
    ExcelReadException,
    FileReaderException,
    FileReadError,
    InfrastructureException,
    JSONReadException,
    PDFReadException,
    ReaderError,
    ResourceNotFoundException,
    TextReadException,
    UnsupportedFormatError,
)


class TestEnterpriseExceptions:
    """Test suite ensuring exception hierarchy and contract meet enterprise standards."""

    def test_base_hierarchy(self):
        """Verify inheritance tree connects to ApplicationException and Exception."""
        assert issubclass(ApplicationException, Exception)
        assert issubclass(BusinessException, ApplicationException)
        assert issubclass(InfrastructureException, ApplicationException)
        assert issubclass(ReaderError, Exception)
        # Backward-compatibility alias
        assert ReaderError is ApplicationException

    def test_business_exceptions_hierarchy(self):
        """Verify domain/business exceptions inherit properly."""
        assert issubclass(UnsupportedFormatError, BusinessException)
        assert issubclass(BusinessValidationException, BusinessException)
        assert issubclass(ResourceNotFoundException, BusinessException)

    def test_infrastructure_exceptions_hierarchy(self):
        """Verify parser/infrastructure exceptions inherit properly."""
        assert issubclass(FileReaderException, InfrastructureException)
        assert issubclass(FileReadError, InfrastructureException)
        assert issubclass(PDFReadException, FileReaderException)
        assert issubclass(CSVReadException, FileReaderException)
        assert issubclass(ExcelReadException, FileReaderException)
        assert issubclass(DOCXReadException, FileReaderException)
        assert issubclass(JSONReadException, FileReaderException)
        assert issubclass(TextReadException, FileReaderException)

    def test_exception_serialization_and_codes(self):
        """Verify error_code and to_dict serialization for API/logging consistency."""
        exc = ApplicationException("Base error message", error_code="CUSTOM_CODE", details={"k": "v"})
        payload = exc.to_dict()

        assert payload["success"] is False
        assert payload["error_code"] == "CUSTOM_CODE"
        assert payload["message"] == "Base error message"
        assert payload["details"] == {"k": "v"}

    def test_file_reader_exception_details(self):
        """Verify file-specific exceptions track file_path in details."""
        exc = PDFReadException("Corrupt PDF header", file_path="sample.pdf")
        assert exc.error_code == "PDF_READ_ERROR"
        assert exc.file_path == "sample.pdf"
        assert exc.details["file_path"] == "sample.pdf"
        assert exc.to_dict()["error_code"] == "PDF_READ_ERROR"

    def test_unsupported_format_error_details(self):
        """Verify UnsupportedFormatError retains extension details and error code."""
        exc = UnsupportedFormatError("Format not supported", extension=".xyz")
        assert exc.error_code == "UNSUPPORTED_FORMAT"
        assert exc.details["extension"] == ".xyz"
        assert exc.to_dict()["error_code"] == "UNSUPPORTED_FORMAT"

    def test_exception_chaining_cause_preserved(self):
        """Verify original exception causes are chained using 'from exc'."""
        original = ValueError("raw underlying failure")
        try:
            raise CSVReadException("Failed to read CSV", file_path="test.csv") from original
        except CSVReadException as caught:
            assert caught.__cause__ is original
            assert isinstance(caught, FileReaderException)
            assert isinstance(caught, InfrastructureException)
            assert isinstance(caught, ApplicationException)
