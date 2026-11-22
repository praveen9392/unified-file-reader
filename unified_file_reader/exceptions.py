"""
Enterprise-grade custom exceptions for unified file reader.

Follows Python Enterprise Exception Handling & Logging Standards:
- SOLID principles and clean architecture
- Single base application exception: ApplicationException (aliased to ReaderError)
- Business vs Infrastructure exception separation
- Proper exception chaining (raise ... from exc)
- Stable error codes and informative error messages
- Backward compatibility with legacy ReaderError, FileReadError, and UnsupportedFormatError
"""

import json
from typing import Any, Dict, Optional


class ApplicationException(Exception):
    """
    Base exception for all application-specific errors.

    All custom exceptions in the unified file reader library inherit from this.
    Supports a stable error_code, a human-readable message, and optional context details.
    """

    default_error_code: str = "APPLICATION_ERROR"

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        Exception.__init__(self, message)
        self.message = message
        self.error_code = error_code or self.default_error_code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary representation for structured logging or API response."""
        data: Dict[str, Any] = {
            "success": False,
            "error_code": self.error_code,
            "message": self.message,
        }
        if self.details:
            data["details"] = self.details
        return data

    def __str__(self) -> str:
        return self.message


# Legacy alias for backward compatibility: ReaderError is an ApplicationException
ReaderError = ApplicationException


# ============================================================================
# Business Exceptions (Domain / Validation / Rules)
# ============================================================================

class BusinessException(ApplicationException):
    """Base exception for all business and domain rule violations."""

    default_error_code: str = "BUSINESS_ERROR"


class UnsupportedFormatError(BusinessException):
    """Raised when attempting to read an unsupported or unrecognized file format."""

    default_error_code: str = "UNSUPPORTED_FORMAT"

    def __init__(
        self,
        message: str,
        extension: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        ctx = dict(details or {})
        if extension:
            ctx["extension"] = extension
        super().__init__(message, error_code=self.default_error_code, details=ctx)


class BusinessValidationException(BusinessException):
    """Raised when validation on input parameters, paths, or data formats fails."""

    default_error_code: str = "VALIDATION_ERROR"


class ResourceNotFoundException(BusinessException):
    """Raised when a requested resource or file cannot be found."""

    default_error_code: str = "RESOURCE_NOT_FOUND"


# ============================================================================
# Infrastructure Exceptions (I/O, Parsing, Third-party Libraries, Engine)
# ============================================================================

class InfrastructureException(ApplicationException):
    """Base exception for technical, parser, or I/O infrastructure failures."""

    default_error_code: str = "INFRASTRUCTURE_ERROR"


class FileReaderException(InfrastructureException):
    """Base exception for file parsing and extraction failures."""

    default_error_code: str = "FILE_READ_ERROR"

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        code = error_code or self.default_error_code
        ctx = dict(details or {})
        if file_path:
            ctx["file_path"] = file_path
        self.file_path = file_path
        ApplicationException.__init__(self, message, error_code=code, details=ctx)


# Legacy alias for backward compatibility
FileReadError = FileReaderException


class PDFReadException(FileReaderException):
    """Raised when reading or parsing a PDF document fails."""

    default_error_code: str = "PDF_READ_ERROR"


class CSVReadException(FileReaderException):
    """Raised when reading or parsing a CSV document fails."""

    default_error_code: str = "CSV_READ_ERROR"


class ExcelReadException(FileReaderException):
    """Raised when reading or parsing an Excel (XLSX) document fails."""

    default_error_code: str = "EXCEL_READ_ERROR"


class DOCXReadException(FileReaderException):
    """Raised when reading or parsing a DOCX (Microsoft Word) document fails."""

    default_error_code: str = "DOCX_READ_ERROR"


class JSONReadException(FileReaderException, json.JSONDecodeError):
    """Raised when reading or parsing a JSON document fails."""

    default_error_code: str = "JSON_READ_ERROR"

    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        doc: str = "",
        pos: int = 0,
    ) -> None:
        json.JSONDecodeError.__init__(self, message, doc, pos)
        FileReaderException.__init__(
            self,
            message=message,
            file_path=file_path,
            error_code=error_code,
            details=details,
        )


class TextReadException(FileReaderException):
    """Raised when reading or decoding a plain text document fails."""

    default_error_code: str = "TEXT_READ_ERROR"
