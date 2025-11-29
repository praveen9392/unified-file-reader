"""
Abstract base reader interface.

Defines the contract that all concrete readers must implement.
Follows Interface Segregation Principle (ISP) and Liskov Substitution Principle (LSP).
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseReader(ABC):
    """
    Abstract base class for all file readers.

    All concrete reader implementations must inherit from this class
    and implement the required methods.
    """

    @abstractmethod
    def can_read(self, extension: str) -> bool:
        """
        Check if this reader can handle the given file extension.

        Args:
            extension: File extension (e.g., ".csv")

        Returns:
            True if this reader supports the extension, False otherwise
        """
        pass

    @abstractmethod
    def read(self, path: str) -> Any:
        """
        Read and return the contents of a file.

        Args:
            path: Path to the file to read

        Returns:
            File contents (type depends on the reader implementation)

        Raises:
            FileNotFoundError: If file does not exist
            Exception: If file cannot be read or parsed
        """
        pass
